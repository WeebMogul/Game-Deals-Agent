FROM python:3.12.4
WORKDIR /app

RUN pip install --no-cache-dir \
    google-adk\
    python-dotenv\
    requests
COPY . .
EXPOSE 80
CMD ["adk", "api_server","--host", "0.0.0.0", "--port", "80"]
