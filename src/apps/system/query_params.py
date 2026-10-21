from typing import Optional
from fastapi import Query #查询参数

class PaginationQueryParams():
    def __init__(self,
                 page:int=Query(default=1,description='页码'),
                 page_size:int=Query(default=5,description='每页数量',ge=1,le=10))->None:
        self.page=page
        self.page_size=page_size

#?username=zhang&nick_name=张&is_active=true   比如前端发来的是这个
class UserQueryParams():
    def __init__(self,
                 username:Optional[str]=Query(default=None,description='用户名'),  #Optional用来声明一个值允许是指定类型，也允许是None
                 nick_name:Optional[str]=Query(default=None,description='姓名中文名'),
                 is_active:Optional[bool]=Query(default=True,description='状态')
                 )->None:
        self.username=username
        self.nick_name=nick_name
        self.is_active=is_active

    def to_query_params(self):
        query_params={}
        for item,value in self.__dict__.items():   #item是属性名，value是属性值
            if value:
                if item=='is_active':
                    query_params.update({'is_active':value})
                else:
                    query_params.update({item+'__icontains':value})   #'__icontains'是告诉orm，按‘包含’查询，并且忽略大小写
        return query_params    #返回一个字典
