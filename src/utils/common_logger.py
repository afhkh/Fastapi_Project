import time
from loguru import logger
from src.settings import setting

def get_logger():
    #1.判断logs文件夹是否存在，如果不存在，就创建
    log_path=setting.BASE_DIR.joinpath("logs") #joinpath是在此路径上拼接子路径 得到根路径/logs
    log_path.mkdir(parents=True,exist_ok=True)

    #2.设置info级别和error级别日志文件，放在不同文件中
    #在此路径下根据时间来创建两个分别以info和error开头的log文件
    log_path_info=log_path.joinpath(f"info_{time.strftime('%Y-%m-%d')}.log")
    log_path_error=log_path.joinpath(f"error_{time.strftime('%Y-%m-%d')}.log")

    #3.设置这两个文件的自动清理：1.info级别日志,每天00：00 创建一个新的 3天一清理 2.error级别日志4星期清理一次，500m以后创建一个新文件存
    logger.add(
        log_path_info,
        rotation="00:00",
        retention="3 days",
        mode='a+',
        encoding="UTF-8",
        level="INFO",
        format="{name}:{function}:{line} | {message}"
    )
    logger.add(
        log_path_error,
        rotation="500 MB",
        retention="4 weeks",
        mode='a+',
        encoding="UTF-8",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}"
    )
    return logger


get_logger()