docker build -t mineriadatos .
docker run -it --rm --publish 5000:80 --name mineriadatos mineriadatos