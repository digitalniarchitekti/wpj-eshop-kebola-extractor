FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/

CMD ["pip","install","-r","/code/requirements.txt"]

CMD ["python", "-u", "/code/main.py"]
