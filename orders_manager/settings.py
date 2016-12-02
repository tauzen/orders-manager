import os

BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")

ORDER_MANGER_EXCHANGE_NAME = "order-manager"

SHIPMENTS_QUEUE_NAME = "shipments"
SHIPMENTS_ROUTING_KEY = "shipments"

ITEMS_QUEUE_NAME = "items"
ITEMS_ROUTING_KEY = "items"

COMMANDS_EXCHANGE_NAME = "commands"
COMMANDS_EXCHANGE_TYPE = "topic"
