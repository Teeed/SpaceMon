FROM python:3-alpine
EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app/
# RUN apk update && \
# 	apk add --no-cache --virtual .build-deps openssl-dev musl-dev libffi-dev build-base && \
RUN pip install --no-cache-dir -r requirements.txt 
	#apk del .build-deps

RUN pip install gunicorn

COPY modules /app/modules
COPY *.py /app/
COPY config* /app/
COPY localconfig* /app/

CMD gunicorn --bind 0.0.0.0:8000 --workers=2 application:app
