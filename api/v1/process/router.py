from fastapi import APIRouter
from api.v1.process.routes.upload.upload_file import (
    process_router as upload_process_router,
)
from api.v1.process.routes.upload.upload_qa import process_router as qa_process_router
from api.v1.process.routes.upload.upload_text import (
    process_router as text_process_route,
)
from api.v1.process.routes.my_data_sources import my_data_sources_router

router = APIRouter(prefix="/process", tags=["Process"])
router.include_router(upload_process_router)
router.include_router(qa_process_router)
router.include_router(text_process_route)
router.include_router(my_data_sources_router)
