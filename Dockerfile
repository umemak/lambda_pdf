FROM amazonlinux:latest

RUN yum install python3 -y
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python3
RUN mkdir /home/deploy
