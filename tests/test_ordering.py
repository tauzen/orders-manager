from arrow import Arrow
from uuid import uuid4, UUID
from unittest import mock

from orders_manager.ordering import Ordering
from orders_manager.messages import CreateShipment, MessageTypes


def test_add_pending_shipment_adds_pending_order():
    uuid = uuid4()
    now = Arrow.now()
    ordering = Ordering(mock.Mock())

    ordering.add_pending_shipment(uuid, now)

    assert ordering.pending_orders[uuid] == now


def test_add_pending_shipment_one_order_per_uuid():
    uuid_1 = uuid4()
    uuid_2 = UUID(uuid_1.hex)
    ordering = Ordering(mock.Mock())

    ordering.add_pending_shipment(uuid_1, Arrow.now())
    ordering.add_pending_shipment(uuid_2, Arrow.now())

    assert len(ordering.pending_orders) == 1
    assert ordering.pending_orders[uuid_1]


def test_shipment_ordered():
    uuid = uuid4()
    ordering = Ordering(mock.Mock())
    ordering.pending_orders[uuid] = Arrow.now()

    ordering.shipment_ordered(uuid)

    assert len(ordering.pending_orders) == 0


def test_order_pending():
    uuid1, uuid2 = uuid4(), uuid4()

    ordering = Ordering(mock.Mock())
    ordering.pending_orders[uuid1] = Arrow.now()
    ordering.pending_orders[uuid2] = Arrow.now()

    ordering.order_pending()

    assert ordering.ordering_publisher.ship.call_count == 2
