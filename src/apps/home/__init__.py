from .views.views import router as main_router
from fastapi import APIRouter
home_router=APIRouter()
home_router.include_router(main_router,prefix='/main',tags=['首页核心接口'])
#这一行是将main_router注册进home_router中
#prefix相当于打上总标签   home_router把下面那个main_router收编进来，相当于home_router说部门，main_router 是其中一个员工