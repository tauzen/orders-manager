import json
from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin

from orders_manager import settings
from orders_manager.messages import MessageTypes, ShipmentCreated, ItemPaid


class OrderingSubscriber(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

        exchange = Exchange(settings.ORDER_MANGER_EXCHANGE_NAME, type="topic")
        self.shipments_queue = Queue(
            settings.SHIPMENTS_QUEUE_NAME,
            exchange,
            routing_key=settings.SHIPMENTS_ROUTING_KEY
        )

        self.items_queue = Queue(
            settings.ITEMS_QUEUE_NAME,
            exchange,
            routing_key=settings.ITEMS_ROUTING_KEY
        )

        self.handlers = {}

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                [self.shipments_queue, self.items_queue],
                accept=['json'],
                callback=[self.handle_message]
            )
        ]

    def handle_message(self, body, message):
        message.ack()
        print("Message received - body {}".format(body))
        print("Message received - message {}".format(message))

        event = json.loads(body)
        handler = self.handlers.get(event["type"])
        if not handler:
            print("Handler for type {} not available".format(event["type"]))
            return

        if event["type"] == MessageTypes.shipment_created:
            return handler(ShipmentCreated(**event))
        elif event["type"] == MessageTypes.item_paid:
            return handler(ItemPaid(**event))

    def register_handler(self, event_type, handler):
        assert event_type, handler
        assert event_type in [e for e in MessageTypes]
        self.handlers[event_type] = handler
