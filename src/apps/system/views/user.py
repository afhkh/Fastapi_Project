from fastapi import APIRouter
router=APIRouter()
from ..models import UserInfo,Roles,Job
from ..schemas import LoginRequest,UserInSchema
from typing import List
# from src.apps.system.models import UserInfo

from src.utils.common_exception import LoginException
from .core import get_current_user
from ..schemas import UserSchema
from ..views.core import create_access_token,authenticate_user
#pip install PyJWT[crypto]
#pip install python-jose[cryptography]
from fastapi import Depends
from src.utils.common_response import APIResponse
from ..query_params import PaginationQueryParams,UserQueryParams
from src.utils.common_response import PaginationResponse
#登录，锁定，解锁，修改个人信息.....

###1.用户登录####

@router.post('/login',description='登录接口')
async def login(login_request:LoginRequest):
    #1.1携带用户名密码---》之前封装axios--》规定了编码形式是json
    #1.2根据前端传入的用户名，密码，查询数据库中的用户
    user:UserInfo=await authenticate_user(login_request.username,login_request.password)
    if not user:  #要么不在，要么密码错误
        raise LoginException()
    
    #1.3通过用户，签发token
    token=create_access_token(data={'username':user.username})
    #1.4返回给前端
    return APIResponse(username=user.username,avatar=user.avatar,token=token)


#2. 查询所有用户接口---带分页--带过滤
@router.get("/users",description="查询所有用户")
async def get_user_list(
    page_query:PaginationQueryParams=Depends(),# 查询分页参数，强行转成PaginationQueryParams的对象：page,page_size..
    user_query:UserQueryParams=Depends(), #查询用户参数：根据用户名，用户中文名，是否活跃状态 去查询用户
    user:UserInfo=Depends(get_current_user)
):
    search=user_query.to_query_params()   #返回的那个字典 {nick_name__icontains:刘}
    user=await UserInfo.filter(**search).filter(is_delete=False).all().prefetch_related('roles')  #**search就是把他打散  nick_name__contains='刘'  #这里查的是所有符合的数据，就是UserInfo里面一堆数据对象，故users是一个列表
    #序列化 Pydantic
    user_dicts = [
    UserSchema.model_validate(item).model_dump()    #model_validate(item)：按照 UserSchema 读取并校验对象属性。model_dump()：把校验后的数据转成字典。
    for item in user                               #for item in users：逐个取出用户对象。
    ]
    #返给前端(分页的响应对象)
    return PaginationResponse(data=user_dicts,page=page_query.page,page_size=page_query.page_size)

##3 根据用户id查询用户详情接口
@router.get('/users/{user_id}',description='查询单个用户')
async def get_user_info(
    user_id:int,
    user:UserInfo=Depends(get_current_user)
    ):
    #根据用户id，拿到用户
    user=await UserInfo.filter(id=user_id).prefetch_related('roles').first()
    #使用pydantic序列化
    if user:
        user_dict=UserSchema.model_validate(user).model_dump()
        return APIResponse(result=user_dict)
    #返回给前端
    else:
        raise Exception('该用户不存在')

##4.删除用户：单删和多删------请求体中数据格式
@router.delete('/users',description='删除用户接口，单条多条都支持')
async def delete_user(
    ids:List[int],
    user:UserInfo=Depends(get_current_user)
):
    # res=await UserInfo.filter(id__in=ids).delete() #硬删除，数据库也删除
    res=await UserInfo.filter(id__in=ids).update(is_delete=True) #软删除，字段控制
    print(res)
    return APIResponse(msg='删除成功')

# 5 新增用户
@router.post('/users', description="新增用户接口")
async def create_user(
        user_in: UserInSchema,
        user: UserInfo = Depends(get_current_user)
):
    roles = user_in.roles or []
    jobs = user_in.job or []
    del user_in.roles
    del user_in.job
    password = UserInfo.make_password('123456')
    user_new = await UserInfo.create(**user_in.dict(), password=password)
    for role_id in roles:
        role = await Roles.get(id=role_id)
        await user_new.roles.add(role)
    for job_id in jobs:
        job = await Job.get(id=job_id)
        await user_new.job.add(job)
    return APIResponse(msg='创建成功')


# 6 修改用户
@router.put('/users/{user_id}', description="修改用户接口")
async def update_user(
        user_id: int,
        user_in: UserInSchema,
        user: UserInfo = Depends(get_current_user)
):
    roles = user_in.roles or []
    jobs = user_in.job or []
    del user_in.roles
    del user_in.job
    await UserInfo.filter(id=user_id).update(**user_in.dict())
    user_new = await UserInfo.get(id=user_id)
    await user_new.roles.clear()
    await user_new.job.clear()
    for role_id in roles:
        role = await Roles.get(id=role_id)
        await user_new.roles.add(role)
    for job_id in jobs:
        job = await Job.get(id=job_id)
        await user_new.job.add(job)
    return APIResponse(msg='创建成功')


# 7 重置密码
@router.post('/reset/password/{user_id}', description="重置密码")
async def reset_password(
        user_id: int,
        user: UserInfo = Depends(get_current_user)
):
    await UserInfo.filter(id=user_id).update(password=UserInfo.make_password('123456'))
    return APIResponse(msg='重置密码成功')


# 8 锁定用户 lock
@router.delete('/lock', description="锁定用户")
async def lock_user(
        ids: List[int],
        user: UserInfo = Depends(get_current_user)
):
    await UserInfo.filter(id__in=ids).update(is_active=False)
    return APIResponse(msg='锁定成功')
