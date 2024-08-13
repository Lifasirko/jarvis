FROM python:3.12
RUN apt-get update -y

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./jarvis ./jarvis

CMD ["python3", "./jarvis/manage.py", "runserver", "0.0.0.0:8000"]