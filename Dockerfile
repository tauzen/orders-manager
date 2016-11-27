FROM python:3.5

RUN pip install --upgrade pip

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV PYTHONPATH /app
CMD ["python", "-u", "orders_manager/app.py"]