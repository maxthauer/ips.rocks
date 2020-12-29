FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install Flask
RUN pip install geoip2
RUN pip install ipaddress

COPY . /app 
WORKDIR /app



ENTRYPOINT ["python"]
CMD ["main.py"]