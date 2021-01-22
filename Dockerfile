FROM python:3.8
WORKDIR /var/www/html
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt 
