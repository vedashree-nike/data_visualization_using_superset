import random
import datetime
import json
import time
from kafka import KafkaProducer

# Kafka config
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic_name = 'superset'

products = {
    'Shoes': ['Air Force', 'Air Max', 'Air Jordan', 'Converse'],
    'Apparel': ['Nike Life', 'Nike Club', 'Nike One', 'Nike Drift', 'Nike Tour', 'Nike Pro']
}

cities = ['Delhi', 'Bengaluru', 'Mumbai', 'Kolkata', 'Chennai']
requests = ['Sales Order', 'Purchase Order']
carriers = ['BlueDart', 'FedEx', 'ShadowFax', 'UPS']
ship_methods = ['Roadways', 'Railways', 'Airways']

def random_date(start_date, end_date):
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

def generate_order(order_id):
    category = random.choice(list(products.keys()))
    product = random.choice(products[category])
    from_dc = random.choice(cities)
    to_dc = random.choice([city for city in cities if city != from_dc])
    carrier = random.choice(carriers)
    ship_method = random.choice(ship_methods)
    fulfilment_request = random.choice(requests)

    order_creation_date = random_date(datetime.date(2025, 3, 1), datetime.date(2025, 3, 10))
    modification_date = order_creation_date + datetime.timedelta(days=random.randint(0, 1))
    estimated_shipment_date = order_creation_date + datetime.timedelta(days=1)
    estimated_delivery_date = estimated_shipment_date + datetime.timedelta(days=3)
    actual_shipment_date = estimated_shipment_date + datetime.timedelta(days=random.randint(-1, 1))
    actual_delivery_date = estimated_delivery_date + datetime.timedelta(days=random.randint(-1, 1))

    return {
        'order_id': f"O{order_id:04d}",
        'Product': product,
        'Category': category,
        'fulfilment_request': fulfilment_request,
        'from_dc': from_dc,
        'to_dc': to_dc,
        'carrier': carrier,
        'ship_method': ship_method,
        'order_creation_date': str(order_creation_date),
        'order_modification_date': str(modification_date),
        'estimated_shipment_date': str(estimated_shipment_date),
        'estimated_delivery_date': str(estimated_delivery_date),
        'actual_shipment_date': str(actual_shipment_date),
        'actual_delivery_date': str(actual_delivery_date)
    }

print("Starting producer...")
order_id = 1

try:
    while True:
        order = generate_order(order_id)
        producer.send(topic_name, order)
        print(f"Sent: {order['order_id']}")
        order_id += 1
except KeyboardInterrupt:
    print("Producer stopped.")
    producer.flush()
    producer.close()