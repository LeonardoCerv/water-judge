FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 80

CMD ["uvicorn", "src.judge:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info", "--access-log"]