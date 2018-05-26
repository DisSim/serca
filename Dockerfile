FROM python:3-alpine
MAINTAINER Ryan Birmingham "birm@rbirm.us"

RUN mkdir -p /var/www/serca
COPY . /var/www/serca
WORKDIR /var/www/serca

RUN pip install -r requirements.txt

EXPOSE 5000:5000

CMD python serca.py
