
from pydantic import BaseModel
class LoginRequest(BaseModel):
    username:str
    password:str

class UserSchema(BaseModel):
    id:int
    username:str
    avatar:str
    email:str

    #使用pydantic 把对象转成字典，要带他
    class Config:
        from_attributes=True