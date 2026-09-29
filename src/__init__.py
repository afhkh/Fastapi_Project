from fastapi import FastAPI
from src.apps.home import home_router

def register_router(app:FastAPI):
    app.include_router(home_router,profix='/api/v1/home',tags=['首页所有的路由'])
    #因此home里面的路由前缀为/api/v1/home
    #在这里将home_router注册到app这个路由中

def create_app()-> FastAPI:
    #1.实例化得到app对象
    app=FastAPI()
    #2.注册路由
    register_router(app)
    #3.注册中间件
    #4.注册orm
    #5.注册全局异常
    return app