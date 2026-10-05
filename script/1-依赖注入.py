from fastapi import FastAPI,Depends

app=FastAPI()

##1   函数无参数形式注入
def get_current_user():
    #可以去数据库查用户
    return {'username':'justin'}

#获取用户信息视图函数
@app.get("/get_user/")
async def get_user(current_user:dict =Depends(get_current_user)):
    #以后 在执行get_user视图函数之前，先执行get_current_user,把返回的结果就赋值给current_user
    #以后在视图函数中，current_user就可以直接使用
    return {"code":100,'msg':'成功',"user":current_user}


## 2 函数有参数形式注入
def get_user_age(age:int):
    return {'age':age+10}

        #下面的get_user_age如果前面没有lambda就不能加参数
async def get_user_info(user_age:dict =Depends(lambda:get_user_age(10))):

    return {"code":100,'msg':'成功',"user_age":user_age}


#3.多层依赖注入
#第一个依赖函数
def get_db():
    return "db_connevtion"

#第二个依赖函数.依赖于get_db
def get_user(db=Depends(get_db)):
    return {"user":"test_user","db":db}

@app.get("/data/")
async def data(user_info:dict=Depends(get_user)):
    #请求来了---》先执行get_db-->再执行get_user--->进入视图函数执行
    return {'code':100,'user_info':user_info}


####4.类作为依赖注入####
class DemoClass:
    def __init__(self,q:str=None):
        self.q=q

@app.get('/demo/')
async def demo(commons:DemoClass=Depends()):  #注入的返回类型时DemoClass类型--》会执行类的init
    return {'code':100,'q':commons.q}


    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('1-依赖注入:app',reload=True)