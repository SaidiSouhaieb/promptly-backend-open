from fastapi import APIRouter
from routes.auth.routes.register import register_router


router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(register_router)
