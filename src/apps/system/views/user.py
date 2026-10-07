from fastapi import APIRouter
router=APIRouter()

from pydantic import BaseModel
from datetime import datetime
# from src.apps.system.models import UserInfo
from ..models import UserInfo
from src.utils.common_exception import LoginException
from datetime import timedelta,datetime,timezone
from src.settings import setting
#pip install PyJWT[crypto]
#pip install python-jose[cryptography]
from jose import jwt
from src.utils.common_response import APIResponse
#登录，锁定，解锁，修改个人信息.....

###1.用户登录####


class LoginRequest(BaseModel):
    username:str
    password:str


#根据用户名密码查用户的方法--->内部要异步查数据库，所以是async的
async def authenticate_user(username:str,password:str):
    #先根据用户名查到用户
    user:UserInfo=await UserInfo.get_or_none(username=username)
    #再校验密码
    if not user:  #用户不存在
        return False
    if not user.check_password(password):
        return False
    return user #查到了，密码也对

#根据用户签发token的函数
def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode=data.copy()
    #1.复制一份data数据：用户名，用户相关信息
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta     #datetime.now(timezone.utc)取当前的utc时间
    else:
        #如果没传，用配置文件默认
        expire=datetime.now(timezone.utc)+timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,setting.SECRET_KEY,algorithm=setting.ALGORITHM)
    return encoded_jwt


@router.post('/login')
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
