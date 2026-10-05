
from typing import Optional,Any,Tuple,List
from fastapi import status
from fastapi.responses import JSONResponse
class APIResponse(JSONResponse):
    def __init__(self,code:int=100,msg:Optional[str]='成功',status_code:int=status.HTTP_200_OK,**kwargs)->None:
        self.data={
            'code':code,
            'msg':msg,
        }
        self.data.update(kwargs)
        super().__init__(content=self.data,status_code=status_code)