FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
CMD ["python3", "index.py"]