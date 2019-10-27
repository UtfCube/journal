FROM python:3.7

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install --requirement requirements.txt

WORKDIR /app

ADD . .

RUN chmod +x boot.sh

ENV FLASK_APP journal.py

#RUN flask db upgrade
EXPOSE 8000
ENTRYPOINT ["./boot.sh"]
