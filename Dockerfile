# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY app/ ./app
# COPY frontend/build/ ./frontend/build

# EXPOSE 5000

# CMD ["python", "application.py"]

FROM python:3.11-slim

WORKDIR /app

# Install Node.js and npm for building the React frontend
RUN apt-get update && apt-get install -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY application.py .
COPY app/ ./app
COPY frontend/build/ ./frontend/build
COPY frontend/ ./frontend

# Build React frontend
RUN cd frontend && npm install && npm run build && cd ..

EXPOSE 5000

CMD ["python", "application.py"]

