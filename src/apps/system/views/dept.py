from fastapi import APIRouter,Depends
from .core import get_current_user
from ..models import UserInfo,Dept
from ..schemas import DeptOutSchema,DeptInSchema
from ..query_params import PaginationQueryParams
from src.utils.common_response import APIResponse,PaginationResponse
from typing import List

router=APIRouter()

#1. 查询所有部门，不分页，不需要带page和page_size--》登录才能使用
@router.get('/depts',description='查询所有部门')
async def get_dept_list(
    user:UserInfo=Depends(get_current_user)
):
    #部门，分父级和子级--》到时候要加过滤条件--》只查出没有父级的部门--》最顶级的部门
    depts=await Dept.filter(is_delete=False).all()
    dept_dicts=[DeptOutSchema.model_validate(dept).model_dump() for dept in depts]
    return APIResponse(results=dept_dicts)

# #2.带分页版本的--->不写带分页的--》部门不会很多--》还有子级
# @router.get('/depts',description='查询所有部门')
# async def get_dept_list(
#     page_query:PaginationQueryParams=Depends(),
#     user:UserInfo=Depends(get_current_user)
# ):
#     #部门，分父级和子级--》到时候要加过滤条件--》只查出没有父级的部门--》最顶级的部门
#     #我们认为：把数据库中的数据都查回来  100w条--》再去做序列化--》再分页   害怕数据量太大给服务器内存撑爆
#     #实际上，select * from dept limit=20 ;生成器--》用多少，查多少，不会一次性查回来
#     depts=await Dept.filter().all()
#     dept_dicts=[DeptOutSchema.model_validate(dept).model_dump() for dept in depts]
#     return PaginationResponse(data=dept_dicts,page=page_query.page,page_size=page_query.page_size)


#3.部门新增---{pid_id：1，sub_count：5，name：山东分公司，enabled：true,dept_sort:1}
# # ① 数据库对象 → Pydantic 对象
# data = DeptSchema.model_validate(dept)

# # ② Pydantic 对象 → 字典
# result = data.model_dump()

@router.post('/depts',description='部门新增')
async def add_dept(
    dept:DeptInSchema,
    user:UserInfo=Depends(get_current_user)
):
    dept=await Dept.create(**dept.model_dump())
    if dept:
        return APIResponse(msg='新增部门成功')
    else:
        raise Exception('部门新增失败')


#4.删除部门--》单条和多条
@router.delete('/depts',description='删除部门')
async def delete_dept(
    ids:List[int],#[1,2,3]
    # user:UserInfo=Depends(get_current_user)
):
    res=await Dept.filter(id__in=ids).update(is_delete=True)#软删除
    # res=await Dept.filter(id__in=ids).delete() #硬删除
    return APIResponse(msg='删除部门成功')

#5.查询一个部门
@router.get('/depts/{dept_id}',description='查询单个部门')
async def get_dept(
    dept_id:int #/depts/1-->查询id为1的部门详情
    # user:UserInfo=Depends(get_current_user)
):
    dept=await Dept.filter(id=dept_id).first()
    dept_dict=DeptOutSchema.model_validate(dept).model_dump()
    return APIResponse(msg='部门查找成功',result=dept_dict)


#6.修改一个部门
@router.put('/depts/{dept_id}',description='修改单个部门')
async def get_dept(
    dept_id:int,         #/depts/1-->修改id为1的部门详情
    dept:DeptInSchema
    # user:UserInfo=Depends(get_current_user)
):
    dept=await Dept.filter(id=dept_id).update(**dept.model_dump())
    return APIResponse(msg='部门修改成功')