import os
import sys
import logging

from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from api.v1.chatbots.router import router as chatbot_router
from api.v1.process.router import router as process_router
from db.session import get_db, engine
from sqlalchemy import inspect, text


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

app.include_router(chatbot_router)
app.include_router(process_router)


@app.get("/test-db-connection")  # Fixed: added app. prefix and proper decorator
async def test_db_connection(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {"tables": tables}


@app.get("/")  # Fixed: added app. prefix
async def root():
    return {"message": "API is working", "admin_panel": "/admin"}


if __name__ == "__main__":  # Uncommented and fixed the main block
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8230, reload=True)
