FROM python:3.6
MAINTAINER TimurMardanov timurmardanov97@gmail.com

ENV PYTHONBUFFERED 1
ENV DOCKER_SERVER True


RUN mkdir /practice2018
WORKDIR /practice2018

ADD requirements.txt /practice2018/

RUN pip install -r requirements.txt

ADD . /practice2018/

