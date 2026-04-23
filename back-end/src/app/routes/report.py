from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from services.report_service import generate_interview_report, generate_pdf_report

router = APIRouter()

@router.get("/interview/{interview_id}/report")
def get_report(interview_id: int, db: Session = Depends(get_db)):

    report = generate_interview_report(db, interview_id)

    if not report:
        raise HTTPException(status_code=404, detail="Interview not found or no data")

    return report

@router.get("/interview/{id}/report/pdf")
def download_pdf(id: int, db: Session = Depends(get_db)):
    return generate_pdf_report(db, id)    