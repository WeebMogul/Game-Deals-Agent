FROM python:3.12.4
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 8501 

COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
