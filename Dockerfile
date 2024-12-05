FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8888

RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8888", "app:application"]