from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin

from orders_manager import settings
from orders_manager.messages import (
    MessageTypes,
    messages_parser,
)


class OrderingSubscriber(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

        self.shipments_queue = Queue(
            settings.SHIPMENTS_QUEUE_NAME,
            Exchange(settings.SHIPMENTS_EXCHANGE, type="topic"),
            routing_key=settings.SHIPMENTS_BINDING_ROUTING_KEY
        )

        self.items_queue = Queue(
            settings.ITEMS_QUEUE_NAME,
            Exchange(settings.ITEMS_EXCHANGE, type="topic"),
            routing_key=settings.ITEMS_BINDING_ROUTING_KEY
        )

        self.handlers = {}

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                [self.shipments_queue, self.items_queue],
                accept=['json'],
                callbacks=[self.handle_message]
            )
        ]

    def handle_message(self, body, message):
        message.ack()
        print("Message received - body {}".format(body))

        event = messages_parser(body)
        if event.get("type") not in self.handlers:
            print("Handler for type {} not found".format(event.get("type")))
            return

        handler, cls = self.handlers[event["type"]]
        return handler(cls(**event))

    def register_handler(self, event_type, cls, handler):
        assert event_type, handler
        assert event_type in [e for e in MessageTypes]
        self.handlers[event_type] = (handler, cls)
