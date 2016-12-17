import json
from kombu import Connection, Exchange
from kombu.pools import producers

from orders_manager import settings
from orders_manager.messages import CreateShipment, MessageEncoder


class OrderingPublisher:
    def __init__(self) -> None:
        self.exchange = Exchange(
            settings.COMMANDS_EXCHANGE_NAME,
            "topic"
        )

    def ship(self, command: CreateShipment) -> None:
        print("Creating shipment {}".format(command))
        with Connection(settings.BROKER_URL) as connection:
            with producers[connection].acquire(block=True) as producer:
                producer.publish(
                    json.dumps(command._asdict(), cls=MessageEncoder),
                    content_type="application/json",
                    exchange=self.exchange,
                    declare=[self.exchange]
                )
