import json
import mysql.connector
from kafka import KafkaConsumer

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Lenovo&5678',
    database='orders'
)
cursor = conn.cursor()
print("Connected to MySQL")

# Kafka Consumer
consumer = KafkaConsumer(
    'superset',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening to Kafka topic: superset")

# Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(10) PRIMARY KEY,
    Product VARCHAR(50),
    Category VARCHAR(50),
    fulfilment_request VARCHAR(50),
    from_dc VARCHAR(50),
    to_dc VARCHAR(50),
    carrier VARCHAR(50),
    ship_method VARCHAR(50),
    order_creation_date DATE,
    order_modification_date DATE,
    estimated_shipment_date DATE,
    estimated_delivery_date DATE,
    actual_shipment_date DATE,
    actual_delivery_date DATE
)
"""
cursor.execute(create_table_query)

# Insertion query
insert_query = """
REPLACE INTO orders (
    order_id, Product, Category, fulfilment_request, from_dc, to_dc,
    carrier, ship_method, order_creation_date, order_modification_date,
    estimated_shipment_date, estimated_delivery_date, actual_shipment_date, actual_delivery_date
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

inserted_count = 0

try:
    for message in consumer:
        record = message.value
        try:
            if isinstance(record, list):
                for r in record:
                    values = tuple(r.values())
                    cursor.execute(insert_query, values)
                    inserted_count += 1
            else:
                values = tuple(record.values())
                cursor.execute(insert_query, values)
                inserted_count += 1
            conn.commit()
            print(f" Inserted order: {record['order_id'] if isinstance(record, dict) else 'batch'}")
        except Exception as e:
            print(f" Error inserting record: {e}")
except KeyboardInterrupt:
    print(" Consumer stopped.")
finally:
    print(f" Total inserted: {inserted_count} records.")
    cursor.close()
    conn.close()