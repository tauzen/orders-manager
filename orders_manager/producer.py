from kombu import BrokerConnection
from kombu.pools import producers

from orders_manager import settings
from orders_manager.queues import order_manager_ex

connection = BrokerConnection(settings.BROKER_URL)
with producers[connection].acquire(block=True) as producer:
    producer.publish(
        {"test": "test"},
        serializer="json",
        exchange=order_manager_ex,
        declare=[order_manager_ex],
        routing_key="shipments"
    )

print("Published")
