FROM python:3.10.4-alpine3.15

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python","frontend.py"]