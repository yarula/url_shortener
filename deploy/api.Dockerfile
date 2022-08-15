FROM python:3.7

ENV app shortener_api

RUN mkdir /$app

WORKDIR /$app

ADD src/requirements.txt /$app/

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install --yes vim tcpdump net-tools iputils-ping less && \
    rm -rf /var/lib/apt/lists/*

ADD src /$app/

ENV PYTHONPATH=${VARIABLE_NAME}:/shortener_api

CMD python main.py
