FROM python:3.9

WORKDIR /code

COPY ./requirements.lock.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8080
ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8080"]
