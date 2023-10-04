FROM python:3.11-slim-buster

WORKDIR /code

COPY ./requirements/ /code/requirements/

RUN pip install --no-cache-dir --upgrade -r /code/requirements/dev.txt

COPY . /code

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
