FROM node:20-alpine AS Frontend

WORKDIR /app

COPY ./frontend/package.json ./frontend/package-lock.json* ./
RUN npm install

COPY ./frontend .

EXPOSE 3000

CMD ["npm", "run", "dev"]

FROM python:3.11-slim AS Backend

WORKDIR /app

COPY ./back-end/requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

# THIS IS THE KEY FIX
WORKDIR /app/back-end/src/app

EXPOSE 8000

CMD ["python", "main.py"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

