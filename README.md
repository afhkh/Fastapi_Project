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


引入日志
#1. loguru 是python界非常出名贼简单的一个日志库，很方便的记录日志
#2.引入到我们的项目中
    -用户只要访问我们的接口，我们就记录日志：info日志--》开发阶段
        -日志+中间件
    -用户操作系统处理异常，我们就记录日志：error日志--》上线
        -全局异常处理
#3.安装 配置
    -pip install loguru

中间件
#1.目前先写两个中间件
    -处理cors跨域
    -记录访问日志，统计访问时间，返回到响应头中
        -用户只要访问，记录日志

前端样式库
    -element团队的:elementui  目前Vue3用的话是element-plus 
        -网址：https://element-plus.org/zh-CN/
    
    -蚂蚁团队的：ant-desgin ：区分Vue版本
        -网址https://www.antdv.com/docs/vue/introduce-cn

    -移动端的：vant vue
        -网址https://vant-ui.github.io/vant/#/zh-CN


jwt：json web token 是一种前后端登录认证的方式
    -cookie  保存再客户端浏览器上的键值对
        -用户登录了--》记录用户登录--》向客户端浏览器中写入用户名
        -以后用户访问我们需要登录后才能访问的接口（地址）--》携带当前给的用户名
        -泄露，被篡改--》把张三改成李四--》购物

    -session：：保存再服务端的键值对
        -用户登录了--》记录用户登录--》向客户端浏览器中写入  随机字符串
            {张三：123w46w462，李四：967afsggss，王五：sahfkjasg64}
        -以后用户访问我们需要登录后才能访问的接口（地址）--》携带随机字符串
            -后端，根据随机字符串拿到是谁（django-session：关系型数据：性能：redis）
        
        -不好处：如果登录用户量大，服务端要存储大量的数据，造成压力
    
    -token：不在服务端存储，但是能保证安全的登录认证机制
        -原理：三段式，每段使用base64编码
            asdfasf.asdfasdf.asdfasdfasd
              头      荷载        签名
        -用户登录了--》记录用户登录--》生成一个三段式的token--》返回给客户端
             头一般固定：荷载（用户信息：用户名，token过期时间token签发时间）：签名
             头+荷载通过某个加密方式得到（md5）--》签名
        
        -以后用户访问我们需要登录后才能访问的接口（地址）--》携带token
            -拿出token的头和荷载，再使用之前的加密方式（md5），得到新签名
                -如果这个token没有被改过，这俩签名是一样的--》既然一样--》信赖荷载中用户的信息：用户名
                -如果token被改了，两个签名就不一样了--》不能让用户继续往后走了
                -伪造？  我们不知道签名生成的方案，密钥
    
    -jwt： json web token
        -针对于web方向的token的认证机制


登录  相关表
    -不需要注册--》超级管理员创建的--》我们只能改密码，该信息
    -公司内部项目
    -互联网项目肯定注册：100%要注册

用户表，在线用户表

        

