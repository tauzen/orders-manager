from kombu import Connection
from kombu.mixins import ConsumerMixin

from orders_manager import settings
from orders_manager.queues import shipments_q


class ShipmentsConsumer(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                shipments_q,
                accept=['pickle', 'json'],
                callbacks=[self.on_message])
        ]

    def on_message(self, body, message):
        print("Received msg - body: {}".format(body))
        print("Received msg - message: {}".format(message))
        message.ack()


print("Connecting to exchange")
with Connection(settings.BROKER_URL) as connection:
    ShipmentsConsumer(connection).run()
