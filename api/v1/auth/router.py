from fastapi import APIRouter
from api.v1.auth.routes.register import register_router
from api.v1.auth.routes.login import login_router


router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(register_router)
router.include_router(login_router)
