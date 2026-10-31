"""Rebuild demo business data while retaining existing accounts and passwords."""
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tortoise import Tortoise
from tortoise.transactions import in_transaction
from src.apps.oa.models import Leave
from src.apps.system.models import Dept, Job, Menu, Roles, UserInfo
from src.utils.common_db import DB_ORM_CONFIG


async def main():
    await Tortoise.init(config=DB_ORM_CONFIG)
    try:
        conn = Tortoise.get_connection('default')
        tables = [next(iter(row.values())) for row in await conn.execute_query_dict('SHOW TABLES')]
        backup = {}
        for table in tables:
            if not table.replace('_', '').isalnum():
                raise ValueError('Unexpected table name')
            backup[table] = await conn.execute_query_dict(f'SELECT * FROM `{table}`')
        backup_dir = Path(__file__).resolve().parents[1] / 'backups'
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / f"before_demo_rebuild_{datetime.now():%Y%m%d_%H%M%S_%f}.json"
        with backup_path.open('x', encoding='utf-8') as file:
            json.dump(backup, file, ensure_ascii=False, default=str, indent=2)

        async with in_transaction() as db:
            users = await UserInfo.all().using_db(db).order_by('id')
            if not any(user.username == 'hahage' and user.is_superuser for user in users):
                raise ValueError('The hahage superuser was not found; no data was changed')
            roles = await Roles.all().using_db(db).order_by('id')
            if len(roles) < 3:
                raise ValueError('Expected three existing roles; no data was changed')

            for table in ('oa_roles_menus', 'oa_roles_depts', 'oa_users_jobs'):
                await db.execute_query(f'DELETE FROM `{table}`')
            await Leave.all().using_db(db).delete()
            await UserInfo.all().using_db(db).update(dept_id=None)
            await Menu.all().using_db(db).delete()
            await Dept.all().using_db(db).delete()
            await Job.all().using_db(db).delete()

            company = await Dept.create(name='星辰科技', dept_sort=1, sub_count=5, enabled=True, using_db=db)
            departments = []
            for i, name in enumerate(('研发部', '产品部', '人力资源部', '财务部', '运营部'), 2):
                departments.append(await Dept.create(name=name, pid_id=company.id, dept_sort=i, sub_count=0, enabled=True, using_db=db))
            jobs = []
            for i, name in enumerate(('软件工程师', '产品经理', '人事专员', '财务专员', '运营专员'), 1):
                jobs.append(await Job.create(name=name, enabled=True, job_sort=i, using_db=db))

            root = await Menu.create(name='SystemManagement', title='系统管理', type=0, is_menu=True, menu_sort=1, icon='Setting', sub_count=6, using_db=db)
            office = await Menu.create(name='OfficeManagement', title='办公管理', type=0, is_menu=True, menu_sort=2, icon='OfficeBuilding', sub_count=2, using_db=db)
            page_specs = [
                (root, 'SysInfo', '服务性能', 'admin/Info', '/admin/info', 'Monitor'),
                (root, 'SysUser', '用户管理', 'admin/User', '/admin/user', 'User'),
                (root, 'SysRole', '角色管理', 'admin/Role', '/admin/role', 'UserFilled'),
                (root, 'SysMenu', '菜单管理', 'admin/Menu', '/admin/menu', 'Menu'),
                (root, 'SysDept', '部门管理', 'admin/Dept', '/admin/dept', 'OfficeBuilding'),
                (root, 'SysJob', '岗位管理', 'admin/Job', '/admin/job', 'Suitcase'),
                (office, 'LeaveApply', '请假申请', 'oa/LeaveApplication', '/oa/leave-application', 'Edit'),
                (office, 'LeaveApproval', '请假审批', 'oa/LeaveSP', '/oa/leave-approval', 'Checked'),
            ]
            pages = {}
            for i, (parent, name, title, component, path, icon) in enumerate(page_specs, 1):
                pages[name] = await Menu.create(pid_id=parent.id, name=name, title=title, type=1, is_menu=False, component=component, path=path, icon=icon, menu_sort=i, sub_count=0, using_db=db)
            button_groups = {
                'SysUser': [('add','新增'),('delete','删除'),('lock','停用'),('role','分配角色'),('password','重置密码'),('update','修改')],
                'SysRole': [('add','新增'),('delete','删除'),('role','分配权限'),('update','修改')],
                'LeaveApply': [('add','申请'),('update','修改'),('delete','删除')],
                'LeaveApproval': [('approve','审批')],
            }
            buttons = {}
            for page_name, specs in button_groups.items():
                page = pages[page_name]
                prefix = {'SysUser':'user', 'SysRole':'role', 'LeaveApply':'leave', 'LeaveApproval':'leave'}[page_name]
                for i, (action, label) in enumerate(specs, 1):
                    code = f'{prefix}:{action}'
                    buttons[code] = await Menu.create(pid_id=page.id, name=f'{page_name}_{action}', title=f'{page.title}{label}', type=2, permission=code, is_menu=False, menu_sort=i, sub_count=0, using_db=db)
                await Menu.filter(id=page.id).using_db(db).update(sub_count=len(specs))

            for role, name, level, scope, desc in zip(roles[:3], ('系统管理员', '人事管理员', '普通员工'), (1,2,3), ('全部','全部','本级'), ('管理系统与权限', '处理人员和请假审批', '查看和申请个人请假')):
                await Roles.filter(id=role.id).using_db(db).update(name=name, level=level, data_scope=scope, description=desc, status=True, is_delete=False)
            await roles[0].menus.add(root, office, *pages.values(), *buttons.values(), using_db=db)
            await roles[1].menus.add(root, office, pages['SysUser'], pages['SysDept'], pages['LeaveApply'], pages['LeaveApproval'], *[buttons[x] for x in ('user:add','user:update','user:role','leave:add','leave:approve')], using_db=db)
            await roles[2].menus.add(office, pages['LeaveApply'], *[buttons[x] for x in ('leave:add','leave:update','leave:delete')], using_db=db)
            await roles[0].depts.add(company, *departments, using_db=db)
            await roles[1].depts.add(*departments, using_db=db)
            await roles[2].depts.add(departments[0], using_db=db)

            demo_users = [u for u in users if u.username.startswith('demo_user') and not u.is_delete]
            for i, user in enumerate(demo_users):
                index = i % len(departments)
                await UserInfo.filter(id=user.id).using_db(db).update(dept_id=departments[index].id)
                await user.job.add(jobs[index], using_db=db)
            for i, user in enumerate(demo_users[:25]):
                await Leave.create(owner_id=user.id, reason=('身体不适就医', '处理家庭事务', '年度休假', '个人事项', '参加培训')[i % 5], time=(datetime(2026, 11, 1) + timedelta(days=i)).strftime('%Y-%m-%d'), days=str(1 + i % 3), type=1 + i % 3, status=i % 3, approver='人事管理员' if i % 3 else None, using_db=db)
            admin = next(u for u in users if u.username == 'hahage')
            await Leave.create(owner_id=admin.id, reason='个人事务', time='2026-11-10', days='1', type=2, status=0, using_db=db)
        print('备份文件:', backup_path)
        print('已重建：部门 6，岗位 5，目录和页面 10，按钮权限', len(buttons), '，请假记录', min(len(demo_users),25)+1)
        print('账户与现有密码已保留；hahage 是超级用户。')
    finally:
        await Tortoise.close_connections()


if __name__ == '__main__':
    asyncio.run(main())
