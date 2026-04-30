FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

# THIS IS THE KEY FIX
WORKDIR /app/src/app

EXPOSE 8000

CMD ["python", "main.py"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
