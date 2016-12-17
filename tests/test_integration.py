import json
from kombu import Connection, Exchange, Queue
from kombu.pools import producers
import time

from orders_manager import settings


item_paid_dict = {
    "type": "item.paid",
    "uuid": "bfca9eb194964c49ad75d7a45da3961b",
    "when": "2016-12-03T13:20:24.132437+01:00"
}

shipment_ordered_dict = {
  "type": "shipment.ordered",
  "shipmentUUID": "3eccd1b0c2594c97842df854ff3cdf5d",
  "orderedItemUuid": "bfca9eb194964c49ad75d7a45da3961b",
  "when": "2016-12-03T13:26:51.235203+01:00"
}


def publish_message(msg, exchange_name, routing_key):
    with Connection(settings.BROKER_URL) as connection:
        with producers[connection].acquire(block=True) as producer:
            producer.publish(
                json.dumps(msg),
                content_type="application/json",
                exchange=Exchange(exchange_name, type="topic"),
                routing_key=routing_key
            )


def get_message_from_commands_exchange():
    with Connection(settings.BROKER_URL) as conn:
        ex = Exchange("commands", type="topic")
        q = Queue("commands", exchange=ex, routing_key="#", channel=conn.channel())
        q.declare()
        msg = q.get(no_ack=True)
        return msg.decode() if msg else None


def test_end_2_end_scenario():
    time.sleep(settings.RABBIT_INIT_TIMEOUT)

    # empty commands exchange at the beginning
    assert get_message_from_commands_exchange() is None

    # item paid
    publish_message(
        item_paid_dict,
        exchange_name=settings.ITEMS_EXCHANGE,
        routing_key=settings.ITEMS_QUEUE_NAME
    )

    # wait for item to be ordered
    time.sleep(settings.ORDERING_INTERVAL)

    # check if shipment order was dispatched to commands exchange
    received_message = get_message_from_commands_exchange()
    assert received_message["orderedItemUuid"] == item_paid_dict["uuid"]

    # shipment was ordered
    publish_message(
        shipment_ordered_dict,
        exchange_name=settings.SHIPMENTS_EXCHANGE,
        routing_key=settings.SHIPMENTS_QUEUE_NAME
    )

    time.sleep(2 * settings.ORDERING_INTERVAL)

    # check if pending order was removed and no shipment orders were dispatched
    assert get_message_from_commands_exchange() is None
