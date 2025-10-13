FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade --no-cache-dir -r requirements.txt
RUN pip install python-multipart

EXPOSE 8000
CMD python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload