FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir ".[stream,api]"
ENV PYTHONUNBUFFERED=1
CMD ["python","-m","iot_pm.streaming.producer"]
