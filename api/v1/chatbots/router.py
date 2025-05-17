from fastapi import APIRouter
from api.v1.chatbots.routes.chat import chatbot_router
from api.v1.chatbots.routes.my_chatbots import my_chatbots_router
from api.v1.chatbots.routes.create_chatbot import create_chatbot_router

router = APIRouter(prefix="/chatbots", tags=["Chatbots"])

router.include_router(chatbot_router)
router.include_router(my_chatbots_router)
router.include_router(create_chatbot_router)
