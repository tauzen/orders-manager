from arrow import Arrow
from uuid import uuid4, UUID

from orders_manager.messages import CreateShipment
from orders_manager.order_shipment_channel import OrderShipmentChannel


class Ordering:

    def __init__(self, order_shipment_channel: OrderShipmentChannel) -> None:
        self.order_shipment_channel = order_shipment_channel
        self.pending_orders = {}

    def add_pending_shipment(self, uuid: UUID, when: Arrow) -> None:
        self.pending_orders[uuid] = when
        print("Added pending shipment {}".format(uuid))

    def get_state(self) -> dict:
        return self.pending_orders

    def shipment_ordered(self, ordered_item_uuid: UUID) -> None:
        del self.pending_orders[ordered_item_uuid]
        print("Shipment marked as ordered {}".format(ordered_item_uuid))

    # should be called by celery beat
    def order_pending(self) -> None:
        for uuid in self.pending_orders.keys():
            self.order_shipment_channel.ship(
                CreateShipment(uuid4(), Arrow.now(), 'DHL', uuid)
            )
