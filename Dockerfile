FROM python:3.7

RUN pip install -U pip

WORKDIR /app

ADD requirements.txt /app

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc

RUN pip install -r requirements.txt
