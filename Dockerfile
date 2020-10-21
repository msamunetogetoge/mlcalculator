# FROM alpine:latest

# RUN apk --update-cache \
#     add musl \
#     linux-headers \
#     gcc \
#     g++ \
#     make \
#     gfortran \
#     openblas-dev \
#     python3 \
#     python3-dev\
#     py3-pip\
#     postgresql-libs\
#     musl-dev\
#     postgresql-dev
# ADD . /code/
# COPY ./MLkit ./code
# WORKDIR /code/
# RUN pip3 install --no-cache-dir --upgrade pip 
# RUN pip3 install -r requirements.txt
# COPY ./MLkit ./code
# WORKDIR /code/


FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python -m pip install --upgrade setuptools pip wheel
RUN pip install -r requirements.txt
COPY ./MLkit ./code
WORKDIR /code/