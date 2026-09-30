from fastapi import FastAPI
from src.apps.home import home_router
from src.apps.system import system_router
from src.utils.common_middleware import add_cors_middleware

from src.utils.common_db import register_mysql
from src.utils.common_exception import register_exception

def register_router(app:FastAPI):
    #http://127.0.0.1:8080/api/v1/home/main
    app.include_router(home_router,prefix='/api/v1/home',tags=['首页所有的路由'])
    #因此home里面的路由前缀为/api/v1/home
    #在这里将home_router注册到app这个路由中
    app.include_router(system_router,prefix='/api/v1/system',tags=['系统所有路由'])

def register_middle_ware(app:FastAPI):
    add_cors_middleware(app)

def create_app()-> FastAPI:
    #1.实例化得到app对象
    app=FastAPI()
    #2.注册路由
    register_router(app)
    #3.注册中间件
    register_middle_ware(app)
    #4.注册orm
    register_mysql(app)

    #5.注册全局异常
    register_exception(app)
    return app