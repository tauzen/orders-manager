from arrow import Arrow
from uuid import uuid4, UUID

from orders_manager.messages import CreateShipment, MessageTypes
from orders_manager.ordering_publisher import OrderingPublisher


class Ordering:

    def __init__(self, ordering_publisher: OrderingPublisher) -> None:
        self.ordering_publisher = ordering_publisher
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
        print("Ordering pending items if present")
        for uuid in self.pending_orders.keys():
            self.ordering_publisher.ship(
                CreateShipment(
                    MessageTypes.create_shipment,
                    uuid4(),
                    Arrow.now(),
                    'DHL',
                    uuid
                )
            )
