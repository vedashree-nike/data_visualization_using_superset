import random
import datetime
import json
import time
from kafka import KafkaProducer


products = {
    'Shoes': ['Air Force', 'Air Max', 'Air Jordan', 'Converse'],
    'Apparel': ['Nike Life', 'Nike Club', 'Nike One', 'Nike Drift', 'Nike Tour', 'Nike Pro']
}
country_cities = {
    'USA' : ['New York','Houston','Chicago','Austin','Los Angeles'],
    'CHN' : ['Beijing','Xi An','Guangzhou','Nanjing','Shanghai','Shenzhen'],
    'CAN' : ['Toronto','Vancouver','Calgary','Edmonton'],
    'KOR' : ['Seoul','Busan','Gwangju','Incheon','Ulsan'],
    'BEL' : ['Bruges','Namur','Antwerp','Mechelen'],
    'ESO' : ['Barcelona','Madrid','Valencia','Granada'],
    'DEU' : ['Berlin','Munich','Hamburg','Dersden'],
    'JPN' : ['Tokyo','Osaka','Kobe','Kyoto','Yokoama'],
    'MYS' : ['Malacca','Ipoh','Kuching','Kuantan'],
    'HKG' : ['Kowloon','Yuen Long','Tai Po'],
    'AUS' : ['Sydney','Canberra','Perth','Hobart','Melbourne'],
    'SGP' : ['Yishun','Jurong','Tampines','Bukit Batok'],
    'PHL' : ['Quezon City','Cebu City','Legazpi City','Butuan City'],
    'IND' : ['Mumbai','Bengaluru','Chennai','Delhi','Kolkata'],
    'THA' : ['Phuket','Bangkok','Krabi','Hat Yai','Chiang Mai'],
    'MEX' : ['Mexico City','Durango','Tijuana','Guadalajara'],
    'IDN' : ['Jakarta','Surabaya','Medan','Semarang'],
    'GBR' : ['London','York','Bradford','Bristol','Plymouth'],
    'TUR' : ['Istanbul','Ankara','Izmir','Bursa','Antalya'],
    'ISR' : ['Eilat','Dimona','Bnei Brak']
}

requests = ['Sales Order', 'Purchase Order']
carriers = ['BlueDart', 'FedEx', 'ShadowFax', 'UPS']
ship_methods = ['Roadways', 'Railways', 'Airways']
def random_date(start_date, end_date):
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

def generate_order(order_id):
    category = random.choice(list(products.keys()))
    product = random.choice(products[category])
    country_code = random.choice(list(country_cities.keys()))
    from_dc = random.choice(country_cities[country_code])
    to_dc = random.choice([city for city in country_cities[country_code] if city != from_dc])
    fulfilment_request = random.choice(requests)
    carrier_partner = random.choice(carriers)
    ship_method = random.choice(ship_methods)
    order_creation = random_date(datetime.date(2024, 1, 1), datetime.date(2025, 6, 18))
    order_modification = order_creation + datetime.timedelta(days=random.randint(0, 1))
    estimated_shipment = order_creation + datetime.timedelta(days=1)
    estimated_delivery = estimated_shipment + datetime.timedelta(days=3)
    actual_shipment = estimated_shipment + datetime.timedelta(days=random.randint(-1, 1))
    actual_delivery = estimated_delivery + datetime.timedelta(days=random.randint(-1, 1))

    data = {
        'order': {
            'order_id': f"O{order_id:04d}",
            'product': product,
            'category': category,
            'fulfilment_request': fulfilment_request
        },
        'dc': {
            'dc_id': f"D{order_id:04d}",
            'from_dc': from_dc,
            'to_dc': to_dc,
            'country_code': country_code
        },
        'carrier': {
            'carrier_id': f"C{order_id:04d}",
            'carrier_partner': carrier_partner,
            'shipment_method': ship_method
        },
        'time': {
            'time_id': f"T{order_id:04d}",
            'order_creation': str(order_creation),
            'order_modification': str(order_modification),
            'estimated_shipment': str(estimated_shipment),
            'estimated_delivery': str(estimated_delivery),
            'actual_shipment': str(actual_shipment),
            'actual_delivery': str(actual_delivery)
        }
    }
    return data

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'superset'
order_id = 1
print("Producer started.")

try:
    while True:
        record = generate_order(order_id)
        producer.send(topic_name, record)
        print(f"Sent order {record['order']['order_id']}")
        order_id += 1
        time.sleep(0.0005)
except KeyboardInterrupt:
    print("Producer stopped.")
    producer.flush()
