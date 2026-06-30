FROM python:3.11-slim

EXPOSE 8000

WORKDIR /TODO-API

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver" , "0.0.0.0:8000" ]