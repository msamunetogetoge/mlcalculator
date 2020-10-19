FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python -m pip install --upgrade setuptools pip wheel
RUN pip install -r requirements.txt
ADD . /code/
COPY ./MLkit ./code
WORKDIR /code/