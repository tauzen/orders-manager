from types import FunctionType

from orders_manager.ordering import Ordering
from orders_manager.messages import ShipmentCreated, ItemPaid


def create_shipment_created_handler(ordering: Ordering) -> FunctionType:
    def handler(message: ShipmentCreated) -> None:
        print("Received shipment created event {}".format(message))
        ordering.shipment_ordered(message.orderedItemUUID)

    return handler


def create_item_paid_handler(ordering: Ordering) -> FunctionType:
    def handler(message: ItemPaid) -> None:
        print("Received item paid event {}".format(message))
        ordering.add_pending_shipment(message.uuid, message.when)

    return handler
