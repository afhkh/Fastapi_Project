from fastapi import APIRouter
router=APIRouter()

from src.utils.common_response import APIResponse
@router.get('/menus')  #需要登录后才能访问---》需要依赖注入
async def menus():
    #这里能拿到的是哪个用户---》去数据库查出该用户的菜单权限
    #把菜单权限处理成前端需要的样子---》返回给前端
    #还有按钮权限

