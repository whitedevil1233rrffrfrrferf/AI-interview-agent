import pdfplumber
from repository.resume import create_resume

def extract_text_from_pdf(file):
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def upload_resume(db, file, user_email: str):
    content = extract_text_from_pdf(file)

    resume = create_resume(
        db=db,
        user_email=user_email,
        file_name=file.filename,
        content=content
    )

    return resume