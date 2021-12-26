FROM python:3.9.7

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]