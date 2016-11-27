from kombu import Exchange, Queue

order_manager_ex = Exchange("order-manager", type="topic")
shipments_q = Queue(
    "shipments",
    order_manager_ex,
    routing_key="shipments"
)


exchange_order_manager = Exchange("order-manger", type="topic")
queue_shipments = Queue(
    "shipments",
    exchange_order_manager,
    routing_key="shipments"
)
queue_items = Queue(
    "items",
    exchange_order_manager,
    routing_key="items"
)

exchange_commands = Exchange("commands", type="topic")