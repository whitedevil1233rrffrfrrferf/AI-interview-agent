from collections import Counter
from sqlalchemy.orm import Session
from models.interview_model import Interview
from models.interview_qa_model import InterviewQA as Answer
from schemas.report import InterviewReport, QuestionAnalysis
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import FileResponse

def generate_interview_report(db: Session, interview_id: int):

    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return None

    answers = db.query(Answer).filter(Answer.interview_id == interview_id).all()

    if not answers:
        return None

    question_reports = []
    scores = []
    

    for ans in answers:
        scores.append(ans.score)

        question_reports.append(
            QuestionAnalysis(
                question=ans.question,
                answer=ans.answer,
                score=ans.score,
                feedback=ans.feedback
            )
        )

        

    average_score = sum(scores) / len(scores)
    overall_score = round(average_score, 2)

    # 🎯 Simple verdict logic (you can improve later with AI)
    if overall_score >= 7:
        verdict = "hire"
    elif overall_score >= 5:
        verdict = "maybe"
    else:
        verdict = "no_hire"

    # Optional: pick top recurring themes
   

    return InterviewReport(
        interview_id=interview_id,
        overall_score=overall_score,

        total_questions=len(answers),
        average_score=average_score,
        
        verdict=verdict,
        questions=question_reports
    )

def generate_pdf_report(db: Session, interview_id: int):

    report = generate_interview_report(db, interview_id)

    file_path = f"report_{interview_id}.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Interview Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Score: {report.overall_score}", styles["Normal"]))
    elements.append(Paragraph(f"Verdict: {report.verdict}", styles["Normal"]))

    doc.build(elements)

    return FileResponse(file_path, filename=file_path)    