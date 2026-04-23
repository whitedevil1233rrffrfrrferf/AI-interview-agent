# routes/resume_routes.py

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from utils.auth_utils import get_current_user
from services.resume import upload_resume
from schemas.resume import ResumeResponse

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeResponse)
def upload_resume_api(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    resume = upload_resume(db, file, current_user)
    return resume