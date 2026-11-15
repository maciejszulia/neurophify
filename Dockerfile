FROM python:3.13-slim
COPY neurophify.py /app/neurophify.py
ENTRYPOINT ["python", "/app/neurophify.py"]
