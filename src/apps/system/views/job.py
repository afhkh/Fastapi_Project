from fastapi import APIRouter,Depends
from .core import get_current_user
from ..models import UserInfo,Job
from ..schemas import JobOutSchema,JobInSchema
from ..query_params import PaginationQueryParams
from src.utils.common_response import APIResponse,PaginationResponse
from typing import List

router=APIRouter()

#1. 查询所有岗位，不分页，不需要带page和page_size--》登录才能使用
@router.get('/jobs',description='查询所有岗位')
async def get_job_list(
    user:UserInfo=Depends(get_current_user)
):
    #岗位，分父级和子级--》到时候要加过滤条件--》只查出没有父级的岗位--》最顶级的岗位
    jobs=await Job.filter(is_delete=False).all()
    job_dicts=[JobOutSchema.model_validate(job).model_dump() for job in jobs]
    return APIResponse(results=job_dicts)


#3.岗位新增---{pid_id：1，sub_count：5，name：山东分公司，enabled：true,Job_sort:1}
# # ① 数据库对象 → Pydantic 对象
# data = JobSchema.model_validate(Job)

# # ② Pydantic 对象 → 字典
# result = data.model_dump()

@router.post('/jobs',description='岗位新增')
async def add_job(
    job:JobInSchema,
    user:UserInfo=Depends(get_current_user)
):
    job=await Job.create(**job.model_dump())
    if job:
        return APIResponse(msg='新增岗位成功')
    else:
        raise Exception('岗位新增失败')


#4.删除岗位--》单条和多条
@router.delete('/jobs',description='删除岗位')
async def delete_job(
    ids:List[int],#[1,2,3]
    # user:UserInfo=Depends(get_current_user)
):
    res=await Job.filter(id__in=ids).update(is_delete=True)#软删除
    # res=await Job.filter(id__in=ids).delete() #硬删除
    return APIResponse(msg='删除岗位成功')

#5.查询一个岗位
@router.get('/jobs/{job_id}',description='查询单个岗位')
async def get_job(
    job_id:int #/Jobs/1-->查询id为1的岗位详情
    # user:UserInfo=Depends(get_current_user)
):
    job=await Job.filter(id=job_id).first()
    job_dict=JobOutSchema.model_validate(job).model_dump()
    return APIResponse(msg='岗位查找成功',result=job_dict)


#6.修改一个岗位
@router.put('/jobs/{job_id}',description='修改单个岗位')
async def get_job(
    job_id:int,         #/Jobs/1-->修改id为1的岗位详情
    job:JobInSchema
    # user:UserInfo=Depends(get_current_user)
):
    job=await Job.filter(id=job_id).update(**job.model_dump())
    return APIResponse(msg='岗位修改成功')