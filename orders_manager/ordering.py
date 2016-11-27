from uuid import UUID
from arrow import Arrow

from orders_manager.ordering_publisher import OrderingPublisher


class Ordering:

    def __init__(self, ordering_publisher: OrderingPublisher) -> None:
        pass

    def add_pending_shipment(self, uuid: UUID, when: Arrow) -> None:
        pass

    def get_state(self) -> dict:
        pass

    def shipment_ordered(self, ordered_item_uuid: UUID) -> None:
        pass

    def order_pending(self) -> None:
        pass
