import json
from kombu import Connection, Exchange
from kombu.pools import producers

from orders_manager import settings
from orders_manager.messages import CreateShipment, MessageEncoder


class OrderShipmentChannel:
    def __init__(self) -> None:
        self.exchange = Exchange(
            settings.COMMANDS_EXCHANGE_NAME,
            settings.COMMANDS_EXCHANGE_TYPE
        )

    def ship(self, command: CreateShipment) -> None:
        print("Creating shipment {}".format(command))
        connection = Connection(settings.BROKER_URL)
        with producers[connection].acquire(block=True) as producer:
            producer.publish(
                json.dumps(command, cls=MessageEncoder),
                serializer="json",
                exchange=self.exchange,
                declare=[self.exchange]
            )
