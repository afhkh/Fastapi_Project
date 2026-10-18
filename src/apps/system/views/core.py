from ..models import UserInfo
from datetime import timedelta,datetime,timezone
from src.settings import setting
from fastapi.requests import Request
from jose import jwt
from src.utils.common_exception import AuthException
from fastapi import Depends

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

#3.认证，依赖注入--》所有需要登陆才能访问的接口，必须先执行这个--》drf--》认证类
from fastapi.security import OAuth2PasswordBearer #要求前端请求头中带：Authorization：Bearer token三段式
oauth2=OAuth2PasswordBearer(tokenUrl='token')
async def oauth2_scheme(request:Request):
    try:
        token=await oauth2(request)
        return token
    except Exception as e:
        raise AuthException(msg='您必须携带token')

#4.获取当前登录用户---》使用用户携带的token来拿到
async def get_current_user(token:str=Depends(oauth2_scheme)):
    e=AuthException(msg='token验证失败')
    try:
        payload=jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        username:str=payload.get('username')
        if username is None:
            raise e #从荷载中拿不出用户名，说明验证失败
        #根据用户名拿到当前登录用户
        user=await UserInfo.get_or_none(username=username)
    except Exception:
        raise e

    return user 
    


