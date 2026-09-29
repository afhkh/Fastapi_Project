from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
class APPConfigSettings(BaseSettings):
    load_dotenv() #这句话会把 .env中咱们配置的配置项，动态的映射到APPConfigSettings类中
    #项目基础配置
    APP_HOST:str
    APP_PORT:int
    BASE_DIR:Path=Path(__file__).parent.parent

setting=APPConfigSettings()