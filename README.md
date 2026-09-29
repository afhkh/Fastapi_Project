# Fastapi_Project
# 后端：
#    FastApi，jwt，cors，mysql，websocket
# 前端：
#   Vue3，pinia，vue-router，js，vue-cookies，axios，elemenui-plus[ant-design]


#后端目录结构
    Kong-OA-Backend
        -logs:                          #存放日志
            -                           #访问日志
            -                           # 错误日志
        -migrations:                    #迁移记录，自动生成的
        -src:                           #核心代码
            -apps                       #放一个个的app
                -home                   #首页app
                    -__init__.py        #首页相关的APIRouter
                    -views              #放首页的视图函数
                        -views.py       #真正写视图函数的地址
                    -models.py          # 首页功能会用到的表
                    -schemas.py         #pydantic表模型，序列化反序列化和校验
                -system                 #系统功能，RBAC核心
                    -__init__.py        #权限相关的APIRouter
                    -views              # 放RBAC的视图函数
                        -user.py        #写用户相关视图函数
                        -auth.py        #写权限相关的视图函数
                    -models.py          # 放RBAC会用到的表
                    -schemas.py         #pydantic表模型，序列化反序列化和校验
                -__init__.py            #总的APIRouter
            -libs文件夹                 #后期集成第三方，封装写在这里面
                -阿里大于短信
                -阿里oss
                -七牛云存储
                -MinIo存储
            -utils                      #项目公共功能
                -common_logger          #对logger封装
                -common_middlware       #中间件封装
                -common_response        #响应对象封装
                -common_exception       #全局异常封装
                -comoon_db              #数据库封装
            -__init__.py                #创建FastAPI的app对象和注册路由，中间件，全局异常..
            -settings.py                #项目配置文件，数据库链接地址，跨域配置
        -main.py                        #整个程序的入口
