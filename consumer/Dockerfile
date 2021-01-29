FROM python:3.7-alpine

RUN apk update && apk add --no-cache bash gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
RUN chmod +x wait-for.sh

