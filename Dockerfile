FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/


RUN echo "Python version:" \
 && python --version \
 && echo "Pip version:" \
 && pip --version \
 && echo "Installing dependencies from requirements.txt:" \
 && pip install -r /code/requirements.txt \
 && echo "All installed Python packages:" \
 && pip freeze

CMD ["ls"]
CMD ["python", "-u", "/code/main.py"]
