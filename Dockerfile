FROM quay.io/keboola/docker-custom-python:latest

COPY . /code/
WORKDIR /data/

COPY requirements.txt ./
RUN echo "Python version:" \
 && python --version \
 && echo "Pip version:" \
 && pip --version \
 && echo "Installing dependencies from requirements.txt:" \
 && pip install -r requirements.txt \
 && echo "All installed Python packages:" \
 && pip freeze

CMD ["python", "-u", "/code/main.py"]
