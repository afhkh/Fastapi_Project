from src.settings import setting
from pydantic import BaseModel
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

#角色相关
class RoleOutSchema(BaseModel):
    id:int
    name:str
    leval:int
    description:str
    data_scope:str
    status:bool
    #关联关系：db_table指定中间表的名字
    # depts:list[DeptOutSchema]
    # menus:list[MenuOutSchema]
    class Config:
        from_attributes=True

#角色相关
class RoleInSchema(BaseModel):
    name:str
    leval:int
    description:str
    data_scope:str
    status:bool
    #关联关系：db_table指定中间表的名字
    # depts:list[DeptOutSchema]
    # menus:list[MenuOutSchema]
    class Config:
        from_attributes=True

class MenuInSchema(BaseModel):
    pid_id:int|None=None
    sub_count:int|None=None
    #0 菜单 1子菜单 2 按钮
    type:int
    title:str
    name:str
    component:str
    menu_sort:int
    icon:str
    path:str
    i_frame:bool
    cache:bool
    hidden:bool
    permission:str
    is_menu:bool

    class Config:
        from_attributes=True

#菜单相关
class MenuOutSchema(BaseModel):
    id:int
    sub_count:int|None=None
    #0 菜单 1子菜单 2 按钮
    type:int
    title:str
    name:str
    component:str|None=None
    menu_sort:int|None=None
    icon:str|None=None
    path:str|None=None
    i_frame:bool
    cache:bool
    hidden:bool
    permission:str|None=None
    is_menu:bool

    class Config:
        from_attributes=True
    

