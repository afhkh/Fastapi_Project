from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

#1.定义一些自定义异常类
class AuthException(Exception):
    def __init__(self, code:int=None,msg:str=None):
        self.code=code or 1001
        self.msg =msg or '用户认证失败'


class LoginException(Exception):
    def __init__(self, code:int=None,msg:str=None):
        self.code=code or 1002
        self.msg =msg or '用户名或密码错误'


#2.注册异常

def register_exception(app:FastAPI):
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request:Request,exc:AuthException):
        return JSONResponse({'code':exc.code,'msg':exc.msg})

    @app.exception_handler(LoginException)
    async def login_exception_handler(request:Request,exc:LoginException):
        return JSONResponse({'code':exc.code,'msg':exc.msg})

    #可以写非常多，没有权限异常，数据校验异常，数据不存在异常....

    #其他：除了上面处理的以外，会走到这里
    @app.exception_handler(Exception)
    async def common_exception_handler(request:Request,exc:Exception):
        return JSONResponse({'code':9999,'msg':f'服务器异常，请联系系统管理员{str(exc)}'})