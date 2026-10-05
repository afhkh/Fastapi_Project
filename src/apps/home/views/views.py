from fastapi import APIRouter
from fastapi.requests import Request
router=APIRouter()

from src.utils.common_logger import logger
from fastapi.responses import JSONResponse
import psutil

# @router.get('/info')
# async def info():
#     return 'info'

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
# from src.utils.common_response import APIResponse
# @router.get('/cpu')
# async def info():
#     cpu_percent=psutil.cpu_percent(interval=1)
#     cpu_count=psutil.cpu_count(logical=False)
#     #取出cpu核数和cpu占用率
#     # return JSONResponse({'code':100,'msg':'请求成功','data':{'cpu_count':cpu_count,'cpu_percent':cpu_percent}})
#     return APIResponse(data={'cpu_count':cpu_count,'cpu_percent':cpu_percent})

#完整的显示服务器性能的接口
from src.utils.common_response import APIResponse
@router.get('/info')
async def info():

    # 1.1项目运行的操作系统平台 -macos  linux  win10...
    def get_os_info():
        import platform
        return platform.system()+"=="+platform.release()
    # 1.2cpu使用率和总个数
    def get_cpu_info():
        return{
            'percent':psutil.cpu_percent(interval=1),
            'count':psutil.cpu_count()
        }
    # 1.3磁盘信息
    def get_disk_info():
        disk_usage=psutil.disk_usage('C:\\')
        return{
            'total':disk_usage.total / (1024.0 ** 3), #总共多少G
            'used':disk_usage.used / (1024.0 ** 3),     #使用了多少G
            'free':disk_usage.free / (1024.0 ** 3),      #还剩多少G
            'percent':disk_usage.percent
        }
    # 1.4内存使用率
    def get_memory_info():
        mem=psutil.virtual_memory()
        return{
            'total':mem.total / (1024.0 ** 3), 
            'used':mem.used / (1024.0 ** 3),     
            'free':mem.free / (1024.0 ** 3),      
            'percent':mem.percent
        }
    # 1.5网卡流量信息 -进出
    def get_network_info():
        net_io=psutil.net_io_counters()
        return{
            'bytes_sent':net_io.bytes_sent,
            'bytes_recv':net_io.bytes_recv
        }

    system_info={
        'os':get_os_info(),
        'cpu':get_cpu_info(),
        'disk':get_disk_info(),
        'memory':get_memory_info(),
        'network':get_network_info()
    }
    
    return APIResponse(data=system_info)