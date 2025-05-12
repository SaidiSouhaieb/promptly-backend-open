from fastapi import APIRouter
from api.v1.process.routes.upload_file import process_router as text_process_router
from api.v1.process.routes.upload_qa import process_router as qa_process_router
from api.v1.process.routes.upload_text import process_router as text_process_route

router = APIRouter(prefix="/process", tags=["Process"])
router.include_router(text_process_router)
router.include_router(qa_process_router)
router.include_router(text_process_route)


# please
