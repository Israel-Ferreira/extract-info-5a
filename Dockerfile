FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

RUN mkdir temp

COPY . .

RUN pwd

CMD ["python", "main.py"]

