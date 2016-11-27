from collections import OrderedDict
from kombu import Connection
from kombu.mixins import ConsumerProducerMixin

from orders_manager import settings
from orders_manager.queues import (
    exchange_commands,
    queue_items,
    queue_shipments,
)


class OrdersManager(ConsumerProducerMixin):

    def __init__(self, connection):
        self.connection = connection

        self.pendingOrders = OrderedDict()

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queue_shipments,
                accept=['json'],
                callbacks=[self.handle_shipments_event]
            ),
            Consumer(
                queue_items,
                accept=['json'],
                callbacks=[self.handle_items_event]
            )
        ]

    def handle_shipments_event(self, body, message):
        message.ack()

        # shipment.ordered
        del self.pendingOrders[body["orderedItemUUID"]]
        print(self.pendingOrders)

    def handle_items_event(self, body, message):
        message.ack()

        # item.paid
        self.pendingOrders[body["uuid"]] = body["when"]
        print(self.pendingOrders)

    def publish_command(self, body):
        self.producer.publish(
            body,
            exchange=exchange_commands,
            declare=[exchange_commands],
        )

print("Connecting")
with Connection(settings.BROKER_URL) as connection:
    OrdersManager(connection).run()
