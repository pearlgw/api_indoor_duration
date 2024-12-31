FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD uvicorn app.main:app
CMD ["./venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $HOST_PORT_FASTAPI"]