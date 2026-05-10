FROM python:3.12-slim

WORKDIR /app

COPY psycho/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY psycho/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
