FROM python:3.9.1-buster

COPY ./app /app
COPY requirements.txt ./app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]