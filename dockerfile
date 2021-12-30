FROM python:3.7

MAINTAINER marvisyeh@gmail.com

COPY ./ikea /usr/share/webscribe

VOLUME ["/usr/share/webscribe"]

ENV 

WORKDIR


ADD ./ikea/ikea_scribe.py
ADD ./ikea/pymongo_connect.py
ADD ./ikea/tool.py

RUN 