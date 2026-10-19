###  pip install passlib[bcrypt]  专门生成密文密码的
from tortoise import Model,fields
from src.utils.common_model import BaseModel

from passlib.context import CryptContext
pwd_context=CryptContext(schemes=['bcrypt_sha256'],deprecated='auto')
#1.用户表
class UserInfo(BaseModel):
    username=fields.CharField(max_length=150,unique=True,description='用户名')
    password=fields.CharField(max_length=255,description='用户密码')
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

    #用户跟角色，多对多
    roles=fields.ManyToManyField('models.Roles',description='用户和角色的关联表',through='oa_users_roles')
    #用户跟部门：一对多，一个部门有多个员工，而一个员工只属于某一个部门
    #用户跟岗位：

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
class OnlineUser(BaseModel):
    brower=fields.CharField(max_length=128,description='浏览器',null=True)
    ip=fields.CharField(max_length=64,description='用户登录ip',null=True)
    key=fields.CharField(max_length=255,description='存用户token',null=True)
    #关联--允许用户多机器登录--》不同公司要求不一样---》只需要按需求实现即可
    user=fields.ForeignKeyField('models.UserInfo',description='和用户的一对多',null=True)

    class Meta:
        table='oa_online_user'

# 菜单表：Menu    部门表：Dept   角色表：Roles  岗位表：Job

class Menu(BaseModel): # 权限
    """
    上级菜单id, 子菜单数目， 菜单类型， 菜单标题， 组件名称， 组件， 排序， 图标， 连接地址， 是否外链， 缓存， 隐藏
    权限
    """
    pid = fields.ForeignKeyField('models.Menu', description='父菜单id', on_delete=fields.SET_NULL, null=True)
    sub_count = fields.IntField(description='子菜单数目', null=True, blank=True)
    # 0 菜单，1 子菜单，2 按钮
    type = fields.IntField(description='菜单类型',  null=True)
    title = fields.CharField(max_length=32, description='菜单标题',  null=True, unique=True)
    name = fields.CharField(max_length=255, description='前端组件名称',  null=True, unique=True)
    component = fields.CharField(max_length=255, description='前端组件',  null=True)
    menu_sort = fields.IntField(description='菜单排序',  null=True)
    icon = fields.CharField(max_length=255,  null=True, description='菜单图标')
    path = fields.CharField(max_length=255,  null=True, description='菜单链接地址')
    i_frame = fields.BooleanField(default=False, description='是否外链')
    cache = fields.BooleanField(default=False, description='缓存')
    hidden = fields.BooleanField(default=False, description='是否隐藏')
    permission = fields.CharField(max_length=255, description='权限',  null=True)
    is_menu = fields.BooleanField(default=False, description='是否是菜单')

    class Meta:
        table = 'oa_menu'


    def __str__(self):
        return self.title

class Dept(BaseModel):
    """
    id, 父部门id, 子部门数目, name,
    """
    pid = fields.ForeignKeyField('models.Dept', description='父部门id', null=True,  on_delete=fields.SET_NULL)
    sub_count = fields.IntField(null=True, description='子部门数量')
    name = fields.CharField(max_length=64, description='部门名', unique=True)
    enabled = fields.BooleanField(default=True, description='状态')
    dept_sort = fields.IntField(description='排序',  null=True)

    class Meta:
        table = 'oa_dept'

    def __str__(self):
        return self.name


class Roles(BaseModel):
    """
    name, 级别， 描述， 数据权限，
    """
    name = fields.CharField(max_length=32, description='角色名',  null=True, unique=True)
    level = fields.IntField(description='角色级别',  null=True)
    description = fields.CharField(max_length=255, description='描述信息',  null=True)
    data_scope = fields.CharField(max_length=32, description='权限描述,唯一编码',  null=True)
    status = fields.BooleanField(default=True, description='是否启用?状态：1启用、0禁用')
    # 关联关系：table 指定中间表的名字
    depts = fields.ManyToManyField('models.Dept', through='oa_roles_depts', description='角色和部门的关联表')
    menus = fields.ManyToManyField('models.Menu', through='oa_roles_menus', description='角色和菜单的关联表')

    class Meta:
        table = 'ao_role'

    def __str__(self):
        return self.name


class Job(BaseModel):
    """
    岗位名称， 岗位状态， 排序，
    """
    name = fields.CharField(max_length=32, description='岗位名称',  null=True)
    enabled = fields.BooleanField(description='岗位状态', default=False)
    job_sort = fields.IntField(description='排序',  unique=True)

    class Meta:
        table = 'oa_job'

    def __str__(self):
        return self.name
