FROM python:3.10.2-slim-buster

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

CMD ["python", "app.py"]
