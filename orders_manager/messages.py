import arrow
from enum import Enum
from json import JSONEncoder
from typing import NamedTuple
from uuid import UUID


class MessageTypes(Enum):
    create_shipment = "shipment.order"
    shipment_created = "shipment.ordered"
    item_paid = "item.paid"


CreateShipment = NamedTuple(
    'CreateShipment', [
        ('type', MessageTypes),
        ('shipmentUUID', UUID),
        ('when', arrow.Arrow),
        ('supplier', str),
        ('orderedItemUuid', UUID),
    ],
)

ShipmentCreated = NamedTuple(
    'ShipmentCreated', [
        ('type', MessageTypes),
        ('shipmentUUID', UUID),
        ('orderedItemUuid', UUID),
        ('when', arrow.Arrow),
    ],
)

ItemPaid = NamedTuple(
    'ItemPaid', [
        ('type', MessageTypes),
        ('uuid', UUID),
        ('when', arrow.Arrow),
    ]
)


class MessageEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        if isinstance(obj, arrow.Arrow):
            return str(obj)

        if isinstance(obj, MessageTypes):
            return obj.value

        return JSONEncoder.default(self, obj)


def messages_parser(obj: dict) -> dict:
    for key, value in obj.items():
        if "uuid" in key.lower():
            obj[key] = UUID(value)
        elif key == "when":
            obj[key] = arrow.get(value)
        elif key == "type":
            obj[key] = MessageTypes(value)
    return obj
