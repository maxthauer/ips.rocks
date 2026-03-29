FROM python:3.12-trixie
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

RUN pip install Flask
RUN pip install Flask-SSLify
RUN pip install geoip2
RUN pip install ipaddress

COPY . /app 
WORKDIR /app



ENTRYPOINT ["python"]
CMD ["main.py"]
