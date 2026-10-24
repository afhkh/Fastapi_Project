from src.settings import setting
from pydantic import BaseModel
from typing import List

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
    #后期还要动--》有子关系--》递归序列化
    #使用pydantic把对象转成字典，要带它
    class Config:
        from_attributes=True

#反序列化的--》前端给我们的
#序列化的类--》给前端的用的
class DeptInSchema(BaseModel):
    pid_id:int | None=None
    name:str
    enabled:bool
    sub_count:int
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
    id:int
    name:str
    enabled:bool
    job_sort:int

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
