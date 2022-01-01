FROM python:3.7

MAINTAINER marvisyeh@gmail.com

ADD ./ikea /webscap

WORKDIR /webscrap

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3","ikea_scribe.py"]
