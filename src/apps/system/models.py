###  pip install passlib[bcrypt]  专门生成密文密码的
from tortoise import Model,fields

from passlib.context import CryptContext
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
#1.用户表
class UserInfo(Model):
    username=fields.CharField(max_length=150,unique=True,description='用户名')
    password=fields.CharField(max_length=128,description='用户密码')
    #用户输入错误3次密码后，锁定用户--》锁7天--》自动解锁--》超级管理员手动解锁
    is_active=fields.BooleanField(default=True,description='是否是活跃用户')
    email=fields.CharField(max_length=32,description='邮箱',null=True)
    """
    id,和部门是一对多，昵称，性别，手机号，头像，密码，状态，创建者，更新者，创建时间，更新时间，修改密码时间
    """
    nick_name=fields.CharField(max_length=32,description='用户昵称',null=True,unique=True) #null=True表示可以为空
    gender=fields.CharField(max_length=16,description='性别',null=True)
    phone=fields.CharField(max_length=11,description='电话号码',null=True,unique=True)
    avatar=fields.CharField(max_length=64,default='avatar/default.png',description='头像')
    #用户刚创建（超级管理员），是禁用状态，用户修改密码后，才是启用状态，没启用，登录不进去
    enabled=fields.BooleanField(default=True,description='是否启用？状态：1启用，0禁用')
    is_superuser=fields.BooleanField(default=False,description='是否是超级用户')


    class Meta:
        table='oa_users'   #表名

    #数据库设计的三大范式--》数据库的每一个字段必须是最小单位，不能 再分割了--》不会出现list  字典
    #list: 一对多的关系

    def __str__(self):
        return self.username

    #没有注册功能--》有创建用户功能--》管理员用的密码是明文密码--》存到数据库需要是密文密码
    #类上写一个方法--》通过明文得到密文密码的方法--》类的方法--》创建一个用户的时候，还没有对象，只有类
    #类上的方法 staticmethod.（普通函数，类对象都可以用，没有自动传值） classmethod.（类来的调用，会自动把类传入） 对象的方法（对象来调用，会自动把对象传入）
    @classmethod
    def make_password(cls,password:str):
        #返回密文密码-->有个加密方式-->专门的模块去做
        return pwd_context.hash(password)



    #有登录功能--》用户携带明文密码过来--》需要验证跟数据库中密文是否一样
    #写一个方法--》校验明文密码是否正确--》对象的方法--》就要校验这个对象的密码是否正确  对象来调用
    def check_password(self,password:str):
        return pwd_context.verify(password,self.password)



#2.在线用户表
class OnlineUser(Model):
    brower=fields.CharField(max_length=128,description='浏览器',null=True)
    ip=fields.CharField(max_length=64,description='用户登录ip',null=True)
    key=fields.CharField(max_length=255,description='存用户token',null=True)
    #关联--允许用户多机器登录--》不同公司要求不一样---》只需要按需求实现即可
    user=fields.ForeignKeyField('models.UserInfo',description='和用户的一对多',null=True)

    class Meta:
        table='oa_online_user'