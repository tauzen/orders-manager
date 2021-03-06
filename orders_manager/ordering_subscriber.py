from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin

from orders_manager import settings
from orders_manager.messages import (
    ItemPaid,
    MessageTypes,
    messages_parser,
    ShipmentCreated,
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
        handler = self.handlers.get(event.get("type"))
        if not handler:
            print("Handler for type {} not found".format(event.get("type")))
            return

        if event["type"] == MessageTypes.shipment_created:
            return handler(ShipmentCreated(**event))
        elif event["type"] == MessageTypes.item_paid:
            return handler(ItemPaid(**event))

    def register_handler(self, event_type, handler):
        assert event_type, handler
        assert event_type in [e for e in MessageTypes]
        self.handlers[event_type] = handler
