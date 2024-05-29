FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app

RUN pip install motor pymongo[snappy,gssapi,srv,tls] pydantic[dotenv]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
