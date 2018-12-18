FROM python:3.7

RUN pip install -U pip

WORKDIR /app

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc

ADD requirements*.txt /app/

RUN pip install -r requirements-dev.txt
