from arrow import Arrow
from json import JSONEncoder
from typing import NamedTuple
from uuid import UUID


CreateShipment = NamedTuple(
    'CreateShipment', [
        ('shipmentUUID', UUID),
        ('when', Arrow),
        ('supplier', str),
        ('orderedItemUuid', UUID),
    ],
)


class MessageEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        if isinstance(obj, Arrow):
            return str(obj)

        return JSONEncoder.default(self, obj)