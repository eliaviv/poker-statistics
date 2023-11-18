FROM python:3.10.9-slim

LABEL maintainer="eli.aviv6@gmail.com"

RUN mkdir /application

RUN mkdir /application/statistics_data

ADD src /application

RUN apt-get update

RUN apt-get install -y curl procps net-tools vim iputils-ping telnet util-linux

RUN pip3 install pip

COPY requirements.txt /application

WORKDIR /application

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "-m", "app"]