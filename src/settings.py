from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List
class APPConfigSettings(BaseSettings):
    load_dotenv() #这句话会把 .env中咱们配置的配置项，动态的映射到APPConfigSettings类中
    #项目基础配置
    APP_HOST:str
    APP_PORT:int
    BASE_DIR:Path=Path(__file__).parent.parent

    #跨域处理
    CORS_ORIGINS:List=["*"]
    CORS_ALLOW_CREDENTIALS:bool=True
    CORS_ALLOW_METHODS:List=["*"]
    CORS_ALLOW_HEADERS:List=["*"]

    #数据库相关
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASSWORD:str
    DB_DATABASE:str='kong_oa'

    #jwt相关
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30   #过期时间
    SECRET_KEY:str='dagakhgayuabgvmz(()9)'  #密钥
    ALGORITHM:str='HS256'   #加密方式


setting=APPConfigSettings()