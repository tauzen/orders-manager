from enum import Enum
from json import JSONEncoder
from typing import NamedTuple
from uuid import UUID

from arrow import Arrow


class MessageTypes(Enum):
    create_shipment = "shipment.order"
    shipment_created = "shipment.ordered"
    item_paid = "item.paid"


CreateShipment = NamedTuple(
    'CreateShipment', [
        ('type', MessageTypes),
        ('shipmentUUID', UUID),
        ('when', Arrow),
        ('supplier', str),
        ('orderedItemUuid', UUID),
    ],
)

ShipmentCreated = NamedTuple(
    'ShipmentCreated', [
        ('type', MessageTypes),
        ('shipmentUUID', UUID),
        ('orderedItemUuid', UUID),
        ('when', Arrow),
    ],
)

ItemPaid = NamedTuple(
    'ItemPaid', [
        ('type', MessageTypes),
        ('uuid', UUID),
        ('when', Arrow),
    ]
)


class MessageEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        if isinstance(obj, Arrow):
            return str(obj)

        if isinstance(obj, MessageTypes):
            return obj.value

        return JSONEncoder.default(self, obj)