from kombu import Connection

from orders_manager import settings
from orders_manager.handlers import (
    create_item_paid_handler,
    create_shipment_created_handler,
)
from orders_manager.messages import MessageTypes
from orders_manager.order_shipment_channel import OrderShipmentChannel
from orders_manager.ordering import Ordering
from orders_manager.ordering_subscriber import OrderingSubscriber

ordering = Ordering(OrderShipmentChannel())
ordering_subscriber = OrderingSubscriber(Connection(settings.BROKER_URL))

item_paid_handler = create_item_paid_handler(ordering)
shipment_created_handler = create_shipment_created_handler(ordering)

ordering_subscriber.register_handler(
    MessageTypes.shipment_created,
    shipment_created_handler
)
ordering_subscriber.register_handler(
    MessageTypes.item_paid,
    item_paid_handler
)

ordering_subscriber.run()
