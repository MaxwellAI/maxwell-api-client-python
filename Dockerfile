# FROM fkrull/multi-python

FROM python:3.8

RUN pip install -U pip

WORKDIR /app

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc

RUN echo "python -m pytest -x -s" >> /root/.bash_history

ADD requirements*.txt /app/

RUN pip install -r requirements-dev.txt

CMD bash
