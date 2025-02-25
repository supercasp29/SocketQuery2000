FROM python:3.9-slim
WORKDIR /app
COPY socket_server.py /app
EXPOSE 9999
CMD ["python", "socket_server.py"]
