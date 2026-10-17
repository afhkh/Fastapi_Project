from ..models import UserInfo
from datetime import timedelta,datetime,timezone
from src.settings import setting
from jose import jwt

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
async def 


