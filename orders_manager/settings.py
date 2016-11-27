import os

BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@docker_ip:5672/")
HOST_IP = os.environ.get("HOST_IP", "127.0.0.1")

SHIPMENTS_EXCHANGE = "shipments"
SHIPMENTS_QUEUE_NAME = "shipments.orders"
SHIPMENTS_BINDING_ROUTING_KEY = "shipments"

ITEMS_EXCHANGE = "items"
ITEMS_QUEUE_NAME = "items.orders"
ITEMS_BINDING_ROUTING_KEY = "items"

COMMANDS_EXCHANGE_NAME = "commands"

RABBIT_INIT_TIMEOUT = int(os.environ.get("RABBIT_INIT_TIMEOUT", 0))
ORDERING_INTERVAL = int(os.environ.get("ORDERING_INTERVAL", 10))
