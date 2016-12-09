from kombu import Connection
from threading import Timer

from orders_manager import settings
from orders_manager.messages import MessageTypes
from orders_manager.message_handlers import (
    create_shipment_created_handler,
    create_item_paid_handler,
)
from orders_manager.ordering import Ordering
from orders_manager.ordering_publisher import OrderingPublisher
from orders_manager.ordering_subscriber import OrderingSubscriber


def schedule_order_pending(ordering: Ordering) -> None:
    ordering.order_pending()
    Timer(
        settings.ORDERING_INTERVAL,
        schedule_order_pending,
        (ordering,)
    ).start()


ordering = Ordering(OrderingPublisher())
ordering_subscriber = OrderingSubscriber(Connection(settings.BROKER_URL))

item_paid_handler = create_item_paid_handler(ordering)
ordering_subscriber.register_handler(
    MessageTypes.item_paid,
    item_paid_handler
)

shipment_created_handler = create_shipment_created_handler(ordering)
ordering_subscriber.register_handler(
    MessageTypes.shipment_created,
    shipment_created_handler
)

if settings.RABBIT_INIT_TIMEOUT:
    print("Waiting for rabbitmq ... {}s".format(settings.RABBIT_INIT_TIMEOUT))
    from time import sleep
    sleep(settings.RABBIT_INIT_TIMEOUT)

print("Scheduling periodic ordering")
schedule_order_pending(ordering)

print("Connecting to rabbitmq {}".format(settings.BROKER_URL))
ordering_subscriber.run()
