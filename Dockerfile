FROM python:2.7
MAINTAINER howardsid xuehuajun@aliyun.com
WOKRDIR /code
ADD . /code
EXPOSE 80
CMD python http_server.py --port=80
