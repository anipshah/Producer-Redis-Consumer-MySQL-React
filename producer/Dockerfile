FROM python:3.7-alpine

RUN apk update && apk add --no-cache bash gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

WORKDIR /producer
COPY . /producer
RUN pip install -r requirements.txt
RUN chmod +x wait-for.sh


