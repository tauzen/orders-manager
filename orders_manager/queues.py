from kombu import Exchange, Queue

order_manager_ex = Exchange("order-manager", type="topic")
shipments_q = Queue(
    "shipments",
    order_manager_ex,
    routing_key="shipments"
)
