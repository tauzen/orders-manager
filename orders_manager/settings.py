import os

BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")
