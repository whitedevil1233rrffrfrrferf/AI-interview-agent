import os
import shutil
from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session

from schemas.interview_schema import StartInterviewRequest, StartInterviewResponse
from services.interview_service import start_interview_service
from infrastructure.db import get_db
from utils.auth_utils import get_current_user
from services.interview_service import get_interview_history

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    role: str = Form(...),
    difficulty: str = Form(...),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    resume_path = None

    if resume:
        file_path = f"{UPLOAD_DIR}/{resume.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        resume_path = file_path
    result = start_interview_service(
        db=db,
        user_id=current_user,
        role=role,              
        difficulty=difficulty,
        resume_path=resume_path   
    )

    return result

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_interview_history(db, current_user)    