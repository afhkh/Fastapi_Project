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
    async def auth_exception_handler(request:Request,exc:LoginException):
        return JSONResponse({'code':exc.code,'msg':exc.msg})