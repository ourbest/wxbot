FROM python:3

RUN mkdir /code/
WORKDIR /code/

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD * .

ENTRYPOINT ['python', 'wxbot.py', 'prod']