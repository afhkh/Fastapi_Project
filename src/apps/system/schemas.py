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
class DeptSchema(BaseModel):
    id:int
    name:str
    enabled:bool
    dept_sort:int
    #后期还要动--》有子关系--》递归序列化
    #使用pydantic把对象转成字典，要带它
    class Config:
        from_attributes=True

