from src.apps.oa.views import router as main_router
from fastapi import APIRouter
oa_router=APIRouter()
oa_router.include_router(main_router,prefix='/oa',tags=['OA核心接口'])