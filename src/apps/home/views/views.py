from fastapi import APIRouter
from fastapi.requests import Request
router=APIRouter()

from src.utils.common_logger import logger

@router.get('/info')
def info():
    return 'info'

#测试日志的使用
@router.get('/logger_demo')
def logger_demo():
    #用户一进来就打印info日志
    logger.info('来了老弟？')


    #如果出了异常，打印error日志
    try:
        1/0
    except Exception as e:
        logger.error(f"出错了，错误是:{str(e)}")
    
    return 'demo'