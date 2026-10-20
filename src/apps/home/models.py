#pip install tortoise-orm[asyncmy]

#在根目录下执行aerich init -t src.utils.common_db.DB_ORM_CONFIG
#初始化数据库aerich init-db
#如果要增加删除字段或者增加表aerich migrate 只生成记录，不迁移数据
#迁移数据  aerich upgrade

#pip install aerich
#pip install tomlkit
from tortoise import Model,fields

    