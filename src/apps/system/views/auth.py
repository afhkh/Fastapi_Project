from fastapi import APIRouter
router=APIRouter()

from src.utils.common_response import APIResponse
from fastapi import Depends
from ..models import UserInfo
#不同用户登录后，显示的侧边栏是不一样的，按钮权限
@router.get('/menus')  #需要登录后才能访问---》需要依赖注入
async def menus(user:UserInfo=Depends(函数)):
    print(user)#就是当前登录用户，到时候，咱们通过当前登录用户，去拿到这个用户的权限
    
    #这里能拿到的是哪个用户---》去数据库查出该用户的菜单权限
    #把菜单权限处理成前端需要的样子---》返回给前端
    nav=[{
        'name':''
    }]
    #还有按钮权限
    #下面表示当前用户有：：sys系统管理，user用户页面：查看所有，新增，删除
    authoritys=['sys:user:list','sys:user:save','sys:user:delete']

    return APIResponse(nav=nav)
