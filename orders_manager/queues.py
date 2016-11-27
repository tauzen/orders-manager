from kombu import Exchange, Queue

order_manager_ex = Exchange("order-manager", type="topic")
