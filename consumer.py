import json
import mysql.connector
from kafka import KafkaConsumer

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Lenovo&5678',
    database='superset'
)
cursor = conn.cursor()
print("Connected to MySQL")

cursor.execute("""
CREATE TABLE IF NOT EXISTS time (
    time_id VARCHAR(10) PRIMARY KEY,
    order_creation TIMESTAMP,
    order_modification TIMESTAMP,
    estimated_shipment TIMESTAMP,
    estimated_delivery TIMESTAMP,
    actual_shipment TIMESTAMP,
    actual_delivery TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS carrier (
    carrier_id VARCHAR(10) PRIMARY KEY,
    carrier_partner VARCHAR(50),
    shipment_method VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dc (
    dc_id VARCHAR(10) PRIMARY KEY,
    from_dc VARCHAR(50),
    to_dc VARCHAR(50),
    country_code VARCHAR(3),
    carrier_id VARCHAR(10),
    FOREIGN KEY (carrier_id) REFERENCES carrier(carrier_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(10) PRIMARY KEY,
    product VARCHAR(50),
    category VARCHAR(50),
    fulfilment_request VARCHAR(50),
    carrier_id VARCHAR(10),
    dc_id VARCHAR(10),
    time_id VARCHAR(10),
    FOREIGN KEY (carrier_id) REFERENCES carrier(carrier_id),
    FOREIGN KEY (dc_id) REFERENCES dc(dc_id),
    FOREIGN KEY (time_id) REFERENCES time(time_id)
)
""")


consumer = KafkaConsumer(
    'superset',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(" Listening for messages...")

try:
    for message in consumer:
        data = message.value
        try:

            cursor.execute("""
            REPLACE INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, tuple(data['time'].values()))


            cursor.execute("""
            REPLACE INTO carrier VALUES (%s, %s, %s)
            """, tuple(data['carrier'].values()))


            dc_values = list(data['dc'].values())
            dc_values.append(data['carrier']['carrier_id'])
            cursor.execute("""
            REPLACE INTO dc VALUES (%s, %s, %s, %s, %s)
            """, tuple(dc_values))


            order_values = list(data['order'].values())
            order_values.extend([data['carrier']['carrier_id'], data['dc']['dc_id'], data['time']['time_id']])
            cursor.execute("""
            REPLACE INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, tuple(order_values))

            conn.commit()
            print(f"Inserted order {data['order']['order_id']}")

        except Exception as e:
            print(f"Error inserting data: {e}")
except KeyboardInterrupt:
    print("Consumer stopped.")

cursor.close()
conn.close()
