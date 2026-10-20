"""向项目配置的数据库添加测试数据，可重复运行，不覆盖已有记录。"""

import asyncio
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tortoise import Tortoise
from tortoise.transactions import in_transaction

from src.apps.system.models import Dept, Job, Menu, Roles, UserInfo
from src.utils.common_db import DB_ORM_CONFIG


MARKER = 'seed_demo'
PASSWORD = 'Demo@123456'


async def seed_data():
    await Tortoise.init(config=DB_ORM_CONFIG)
    created = Counter()
    try:
        async with in_transaction() as db:
            async def ensure(model, defaults=None, **lookup):
                obj, is_new = await model.get_or_create(
                    using_db=db,
                    defaults={
                        'create_by': MARKER,
                        'update_by': MARKER,
                        **(defaults or {}),
                    },
                    **lookup,
                )
                if obj.create_by != MARKER:
                    raise ValueError(f'{model.__name__} 存在同名的非测试记录：{lookup}')
                created[model.__name__] += int(is_new)
                return obj

            company = await ensure(
                Dept, name='测试公司',
                defaults={'sub_count': 4, 'dept_sort': 1, 'enabled': True},
            )
            departments = []
            for index, name in enumerate(('研发', '人事', '财务', '运营'), start=1):
                departments.append(await ensure(
                    Dept, name=f'测试{name}部',
                    defaults={
                        'pid_id': company.id, 'sub_count': 0,
                        'dept_sort': index + 1, 'enabled': True,
                    },
                ))

            latest_job = await Job.all().using_db(db).order_by('-job_sort').first()
            next_sort = latest_job.job_sort + 1 if latest_job else 1
            jobs = []
            for index, name in enumerate(('开发工程师', '人事专员', '会计', '运营专员')):
                jobs.append(await ensure(
                    Job, name=f'测试{name}',
                    defaults={'enabled': True, 'job_sort': next_sort + index},
                ))

            root_menu = await ensure(
                Menu, name='DemoSystem',
                defaults={
                    'title': '测试系统管理', 'type': 0, 'component': 'Layout',
                    'path': '/demo-system', 'menu_sort': 1, 'icon': 'system',
                    'sub_count': 4, 'is_menu': True,
                },
            )
            menu_specs = (
                ('User', '用户', 'user', 3),
                ('Dept', '部门', 'dept', 0),
                ('Role', '角色', 'role', 0),
                ('Job', '岗位', 'job', 0),
            )
            child_menus = []
            for index, (name, title, key, sub_count) in enumerate(menu_specs, start=1):
                child_menus.append(await ensure(
                    Menu, name=f'Demo{name}',
                    defaults={
                        'title': f'测试{title}管理', 'pid_id': root_menu.id,
                        'type': 1, 'component': f'system/{key}/index', 'path': key,
                        'menu_sort': index, 'sub_count': sub_count, 'is_menu': True,
                        'permission': f'sys:{key}:list',
                    },
                ))

            buttons = []
            for index, (name, title, permission) in enumerate((
                ('List', '查看', 'list'),
                ('Save', '新增', 'save'),
                ('Delete', '删除', 'delete'),
            ), start=1):
                buttons.append(await ensure(
                    Menu, name=f'DemoUser{name}',
                    defaults={
                        'title': f'测试用户{title}', 'pid_id': child_menus[0].id,
                        'type': 2, 'menu_sort': index, 'sub_count': 0,
                        'is_menu': False, 'permission': f'sys:user:{permission}',
                    },
                ))

            admin_role = await ensure(
                Roles, name='测试管理员',
                defaults={'level': 1, 'description': '测试数据管理员', 'data_scope': 'ALL'},
            )
            hr_role = await ensure(
                Roles, name='测试人事',
                defaults={'level': 2, 'description': '测试人事角色', 'data_scope': 'DEPT'},
            )
            staff_role = await ensure(
                Roles, name='测试普通员工',
                defaults={'level': 3, 'description': '测试普通员工角色', 'data_scope': 'SELF'},
            )
            await admin_role.depts.add(company, *departments, using_db=db)
            await admin_role.menus.add(root_menu, *child_menus, *buttons, using_db=db)
            await hr_role.depts.add(departments[1], using_db=db)
            await hr_role.menus.add(
                root_menu, child_menus[0], child_menus[1], *buttons[:2], using_db=db,
            )
            await staff_role.menus.add(root_menu, child_menus[0], buttons[0], using_db=db)

            async def ensure_user(username, defaults, role, job):
                # 已有测试账号不重置密码；每个新账号单独生成带盐的密码哈希。
                existing = await UserInfo.filter(username=username).using_db(db).first()
                if existing is None:
                    defaults = {**defaults, 'password': UserInfo.make_password(PASSWORD)}
                user = await ensure(UserInfo, username=username, defaults=defaults)
                await user.roles.add(role, using_db=db)
                await user.job.add(job, using_db=db)

            await ensure_user(
                'demo_admin',
                {
                    'nick_name': '测试管理员', 'email': 'demo_admin@example.com',
                    'dept_id': company.id, 'is_active': True, 'enabled': True,
                    'is_superuser': True,
                },
                admin_role, jobs[0],
            )

            surnames = ('张', '李', '王', '赵', '刘', '陈')
            for index in range(1, 31):
                dept_index = (index - 1) % len(departments)
                username = f'demo_user{index:02d}'
                await ensure_user(
                    username,
                    {
                        'nick_name': f'测试{surnames[(index - 1) % len(surnames)]}同学{index:02d}',
                        'email': f'{username}@example.com',
                        'gender': '男' if index % 2 else '女',
                        'dept_id': departments[dept_index].id,
                        'is_active': index % 6 != 0,
                        'enabled': True, 'is_superuser': False,
                    },
                    hr_role if dept_index == 1 else staff_role,
                    jobs[dept_index],
                )

        config = DB_ORM_CONFIG['connections']['default']['credentials']
        print(f"数据库：{config['host']}:{config['port']}/{config['database']}")
        for model in (UserInfo, Dept, Job, Roles, Menu):
            count = await model.filter(create_by=MARKER).count()
            print(f'{model.__name__}：新增 {created[model.__name__]} 条，测试数据共 {count} 条')
        print(f'新建测试账号的密码：{PASSWORD}')
        print('管理员：demo_admin；普通账号：demo_user01 ~ demo_user30')
    finally:
        await Tortoise.close_connections()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(seed_data())
