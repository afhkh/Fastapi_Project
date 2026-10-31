from src.settings import setting
from pydantic import BaseModel,Field

from typing import List,Any

class LoginRequest(BaseModel):
    username:str
    password:str

class RoleSchema(BaseModel):
    id:int
    name:str
    #使用pydantic 把对象转成字典，要带他
    class Config:
        from_attributes=True

class UserSchema(BaseModel):
    id:int
    username:str
    nick_name:str
    gender:int
    avatar:str   #都带一个固定前缀
    email:str
    phone:str
    is_active:bool
    roles:List[RoleSchema]
    #使用pydantic 把对象转成字典，要带他
    class Config:
        from_attributes=True

    @classmethod
    def model_validate(cls,obj):
        data=super().model_validate(obj)
        data.avatar=f'http://{setting.APP_HOST}:{setting.APP_PORT}/media/{data.avatar}'    #再某个字段前后加固定的前缀
        return data


class UserInSchema(BaseModel):
    username: str
    nick_name: str
    gender: int
    email: str
    phone: int
    is_active: bool
    roles: List[int] | None = []
    dept_id: int | None = None
    job: List[int] | None = []

    
#部门相关序列化
#序列化的类--》给前端的
class DeptOutSchema(BaseModel):
    id:int
    name:str
    enabled:bool
    dept_sort:int
    pid_id:int |None=None
    #后期还要动--》有子关系--》递归序列化
    # children:List['DeptOutSchema']=[]
    children:List[Any]|None=[]

    class Config:
        from_attributes=True

    #自定义方法来调用--》递归序列化
    @classmethod
    async def from_orm_recursive(cls,obj):
        #1.这个obj是一个部门对象--->使用序列化类[DeptOutSchema]---》转成字典
        #坑：dept_dict.children--》不能直接转
        dept_dict=cls(
            id=obj.id,
            name=obj.name,
            enabled=obj.enabled,
            dept_sort=obj.dept_sort,
            pid_id=obj.pid_id
        ).model_dump(exclude={'children'})
        #2.查出当年部门所有的子部门对象，把children查出来
        children=await obj.children.filter(is_delete=False).all()
        #3.自己转，然后替换
        dept_dict['children']=[await cls.from_orm_recursive(child) for child in children]
        #4.把转化完之后的返回
        return dept_dict


#反序列化的--》前端给我们的
#序列化的类--》给前端的用的
class DeptInSchema(BaseModel):
    pid_id:int | None=None
    name:str
    enabled:bool
    sub_count:int|None=None
    dept_sort:int
    class Config:
        from_attributes=True

class JobOutSchema(BaseModel):
    id:int
    name:str
    enabled:bool
    job_sort:int

    class Config:
        from_attributes=True

class JobInSchema(BaseModel):
    name:str
    enabled:bool
    job_sort:int|None=None

    class Config:
        from_attributes=True



class MenuInSchema(BaseModel):
    pid_id:int|None=None
    sub_count:int|None=None
    #0 菜单 1子菜单 2 按钮
    type:int|None=None
    title:str|None=None
    name:str
    component:str|None=None
    menu_sort:int|None=None
    icon:str|None=None
    path:str|None=None
    i_frame:bool|None=None
    cache:bool|None=None
    hidden:bool|None=None
    permission:str|None=None
    is_menu:bool|None=None

    class Config:
        from_attributes=True

#菜单相关
class MenuOutSchema(BaseModel):
    id:int
    pid_id:int|None=None
    sub_count:int|None=None
    #0 菜单 1子菜单 2 按钮
    type:int|None=None
    title:str|None=None
    name:str
    component:str|None=None
    menu_sort:int|None=None
    icon:str|None=None
    path:str|None=None
    i_frame:bool|None=None
    cache:bool|None=None
    hidden:bool|None=None
    permission:str|None=None
    is_menu:bool|None=None
    children:List[Any]|None=[]

    class Config:
        from_attributes=True

    @classmethod
    async def from_orm_recursive(cls,obj):
        menu_dict=cls(
            id=obj.id,
            pid_id=obj.pid_id,
            sub_count=obj.sub_count,
            type=obj.type,
            title=obj.title,
            name=obj.name,
            component=obj.component,
            menu_sort=obj.menu_sort,
            icon=obj.icon,
            path=obj.path,
            i_frame=obj.i_frame,
            cache=obj.cache,
            hidden=obj.hidden,
            permission=obj.permission,
            is_menu=obj.is_menu
        ).model_dump(exclude={'children'})
        children=await obj.children.filter(is_delete=False).all()
        menu_dict['children']=[await cls.from_orm_recursive(child) for child in children]
        return menu_dict
    

class MenuOutTreeSchema(BaseModel):
    value:int = Field(alias='id')
    label:str = Field(alias='title')
    children:Any |None=[]

    class Config:
        from_attributes=True

    @classmethod
    async def from_orm_recursive(cls,obj):
        obj_dict=cls(
            id=obj.id,
            title=obj.title
        ).model_dump(exclude={'children'})
        children=await obj.children.filter(is_delete=False).all()
        obj_dict['children']=[await cls.from_orm_recursive(child) for child in children]
        return obj_dict

# 角色相关
class RoleOutSchema(BaseModel):
    id: int
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts :  Any | None = []
    menus: Any | None = []

    class Config:
        from_attributes = True

    @classmethod
    async def from_orm_recursive(cls, obj):
        obj_dict = cls(
            id=obj.id,
            name=obj.name,
            level=obj.level,
            description=obj.description,
            data_scope=obj.data_scope,
            status=obj.status
        ).model_dump(exclude={'menus'})
        # depts = await obj.depts.all()
        menus = await obj.menus.all()
        # obj_dict["depts"] = [DeptOutSchema.from_orm(dept).dict() for dept in depts]
        obj_dict["menus"] = [menu.id for menu in menus]
        return obj_dict


class RoleInSchema(BaseModel):
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts : list[DeptOutSchema]
    menus: list[int] | None = []

    class Config:
        from_attributes = True

###给角色功能使用的，查询部门树的序列化类
class DeptOutTreeSchema(BaseModel):
    #序列化时，改别名
    value:int=Field(alias='id')
    label:str=Field(alias='name')
    children:Any | None=[]

    class Config:
        from_attributes=True

    @classmethod
    async def from_orm_recursive(cls,obj):
        obj_dict=cls(
            id=obj.id,
            name=obj.name
        ).model_dump(exclude='children')
        children=await obj.children.all()
        obj_dict['children']=[await cls.from_orm_recursive(child) for child in children]
        return obj_dict



class MenuPermissionSchema(BaseModel):
    name: str
    title: str
    icon: str | None
    path: str | None
    component: str | None
    children: Any | None

    class Config:
        from_attributes = True

    @classmethod
    async def from_orm_recursive(cls, obj, menus_ids=None):
        obj_dict = cls.model_validate(obj).model_dump()
        if menus_ids:
            children = await obj.children.filter(type=1, id__in=menus_ids).all()
        else:
            children = await obj.children.filter(type=1).all()
        obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
        return obj_dict