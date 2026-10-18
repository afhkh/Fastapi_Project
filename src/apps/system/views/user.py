from fastapi import APIRouter
router=APIRouter()
from ..models import UserInfo
from ..schemas import LoginRequest

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


#1. 查询所有用户接口---带分页
@router.get("/users",description="查询所有用户")
async def get_user_list(
    page_query:PaginationQueryParams=Depends(),# 查询分页参数，强行转成PaginationQueryParams的对象：page,page_size..
    user_query:UserQueryParams=Depends(), #查询用户参数：根据用户名，用户中文名，是否活跃状态 去查询用户
    user:UserInfo=Depends(get_current_user)
):
    search=user_query.to_query_params()   #返回的那个字典 {nick_name__icontains:刘}
    users=await UserInfo.filter(**search).all()   #**search就是把他打散  nick_name__contains='刘'  #这里查的是所有符合的数据，就是UserInfo里面一堆数据对象，故users是一个列表
    #序列化 Pydantic
    user_dicts = [
    UserSchema.model_validate(item).model_dump()    #model_validate(item)：按照 UserSchema 读取并校验对象属性。model_dump()：把校验后的数据转成字典。
    for item in users                               #for item in users：逐个取出用户对象。
    ]
    #返给前端(分页)
    return 