FROM python:3.11-slim

WORKDIR /app
COPY notify_ngrok.py .

RUN pip install requests

CMD ["python3", "notify_ngrok.py"]