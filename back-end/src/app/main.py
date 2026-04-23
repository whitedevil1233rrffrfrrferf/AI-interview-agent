from fastapi import FastAPI
import uvicorn
from routes.auth_routes import router as auth_router
from routes.interview_routes import router as interview_router
from routes.interview_qa_routes import router as interview_qa_router
from routes.report import router as report
from infrastructure.db import Base, engine
from core.cors import add_cors_middleware
from models import *

app = FastAPI()

add_cors_middleware(app)
# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(interview_router)
app.include_router(interview_qa_router)
app.include_router(report)

@app.get("/")
def root():
    return {"message": "AI Interview Backend Running"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",   # file_name:app_variable
        host="0.0.0.0",
        port=8000,
        reload=True
    )