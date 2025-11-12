FROM python:3.11-slim
WORKDIR /app
COPY app ./app
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr libtesseract-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r app/requirements.txt
ENV OPENAI_API_KEY=""
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
