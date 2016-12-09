import os

BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@docker_ip:5672/")

SHIPMENTS_EXCHANGE = "shipments"
SHIPMENTS_QUEUE_NAME = "shipments.orders"

ITEMS_EXCHANGE = "items"
ITEMS_QUEUE_NAME = "items.orders"

COMMANDS_EXCHANGE_NAME = "commands"

RABBIT_INIT_TIMEOUT = int(os.environ.get("RABBIT_INIT_TIMEOUT", 0))
ORDERING_INTERVAL = int(os.environ.get("ORDERING_INTERVAL", 10))
