FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY application.py .
COPY app/ ./app

COPY frontend/ ./frontend
RUN cd frontend && npm install && npm run build

EXPOSE 5000

CMD ["python", "application.py"]
