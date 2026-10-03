from fastapi import APIRouter
from fastapi.requests import Request
router=APIRouter()

from src.utils.common_logger import logger
from fastapi.responses import JSONResponse
import psutil

@router.get('/info')
async def info():
    return 'info'

#测试日志的使用
@router.get('/logger_demo')
async def logger_demo():
    #用户一进来就打印info日志
    logger.info('来了老弟？')


    #如果出了异常，打印error日志
    try:
        1/0
    except Exception as e:
        logger.error(f"出错了，错误是:{str(e)}")
    
    return 'demo'

#前后端打通
@router.get('/cpu')
async def info():
    cpu_percent=psutil.cpu_percent(interval=1)
    cpu_count=psutil.cpu_count(logical=False)
    #取出cpu核数和cpu占用率
    return JSONResponse({'code':100,'msg':'请求成功','data':{'cpu_count':cpu_count,'cpu_percent':cpu_percent}})