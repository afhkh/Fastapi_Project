from fastapi import APIRouter,Depends
from .core import get_current_user
from ..models import UserInfo,Menu
from ..schemas import MenuOutSchema,MenuInSchema,MenuOutTreeSchema
from ..query_params import PaginationQueryParams
from src.utils.common_response import APIResponse,PaginationResponse
from typing import List

router=APIRouter()

#1. 查询所有部门，不分页，不需要带page和page_size--》登录才能使用
@router.get('/menus',description='查询所有菜单')
async def get_menu_list(
    # user:UserInfo=Depends(get_current_user)
):
    #部门，分父级和子级--》到时候要加过滤条件--》只查出没有父级的部门--》最顶级的部门
    menus=await Menu.filter(is_delete=False,pid=None).all().prefetch_related('children')
    #子序列化
    menu_dicts=[await MenuOutSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)



#3.部门新增---{pid_id：1，sub_count：5，name：山东分公司，enabled：true,dept_sort:1}
# # ① 数据库对象 → Pydantic 对象
# data = DeptSchema.model_validate(dept)

# # ② Pydantic 对象 → 字典
# result = data.model_dump()

@router.post('/menus',description='菜单新增')
async def add_menu(
    menu:MenuInSchema,
    # user:UserInfo=Depends(get_current_user)
):
    menu=await Menu.create(**menu.model_dump())
    if menu:
        return APIResponse(msg='新增部门成功')
    else:
        raise Exception('菜单新增失败')


#4.删除部门--》单条和多条
@router.delete('/menus',description='删除菜单')
async def delete_menu(
    ids:List[int],#[1,2,3]
    # user:UserInfo=Depends(get_current_user)
):
    res=await Menu.filter(id__in=ids).update(is_delete=True)#软删除
    # res=await Dept.filter(id__in=ids).delete() #硬删除
    return APIResponse(msg='删除菜单成功')

#5.查询一个部门
@router.get('/menus/{menu_id}',description='查询单个菜单')
async def get_menu(
    menu_id:int #/depts/1-->查询id为1的部门详情
    # user:UserInfo=Depends(get_current_user)
):
    menu=await Menu.filter(id=menu_id).first().prefetch_related('children')
    menu_dict=await MenuOutSchema.from_orm_recursive(menu)
    return APIResponse(msg='菜单查找成功',result=menu_dict)


#6.修改一个部门
@router.put('/menus/{menu_id}',description='修改单个菜单')
async def get_menu(
    menu_id:int,         #/depts/1-->修改id为1的部门详情
    menu:MenuInSchema
    # user:UserInfo=Depends(get_current_user)
):
    menu=await Menu.filter(id=menu_id).update(**menu.model_dump())
    return APIResponse(msg='菜单修改成功')

#查询菜单树
@router.get('/tree/menus',description='查询所有菜单')
async def get_menu_list_tree(
    # user:UserInfo=Depends(get_current_user)
):
    menus=await Menu.filter(is_delete=False,pid=None).all().prefetch_related('children')
    menu_dicts=[await MenuOutTreeSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)