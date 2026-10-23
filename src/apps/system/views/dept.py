from fastapi import APIRouter,Depends
from .core import get_current_user
from ..models import UserInfo,Dept
from ..schemas import DeptSchema
from ..query_params import PaginationQueryParams
from src.utils.common_response import APIResponse,PaginationResponse

router=APIRouter()

#1. 查询所有部门，不分页，不需要带page和page_size--》登录才能使用
@router.get('/depts',description='查询所有部门')
async def get_dept_list(
    user:UserInfo=Depends(get_current_user)
):
    #部门，分父级和子级--》到时候要加过滤条件--》只查出没有父级的部门--》最顶级的部门
    depts=await Dept.filter().all()
    dept_dicts=[DeptSchema.model_validate(dept).model_dump() for dept in depts]
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
#     dept_dicts=[DeptSchema.model_validate(dept).model_dump() for dept in depts]
#     return PaginationResponse(data=dept_dicts,page=page_query.page,page_size=page_query.page_size)

#3.部门新增
@router.post('/depts',description='部门新增')
async def add_dept(
    user:UserInfo=Depends(get_current_user)
):
    pass