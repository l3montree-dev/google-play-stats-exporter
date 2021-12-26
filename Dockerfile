FROM python:3.9.7

RUN mkdir app && cd app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]