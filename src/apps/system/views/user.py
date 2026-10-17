from fastapi import APIRouter
router=APIRouter()
from ..models import UserInfo
from ..schemas import LoginRequest

# from src.apps.system.models import UserInfo

from src.utils.common_exception import LoginException

from ..views.core import create_access_token,authenticate_user
#pip install PyJWT[crypto]
#pip install python-jose[cryptography]

from src.utils.common_response import APIResponse
#登录，锁定，解锁，修改个人信息.....

###1.用户登录####

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
