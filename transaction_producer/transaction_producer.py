from kafka import KafkaProducer
import json
import time
import random
from generate_transaction import generate_transaction


producer = KafkaProducer(
    bootstrap_servers='kafka01:29192,kafka02:29292,kafka03:29392',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    transaction = generate_transaction()
    producer.send('payment-transactions', value=transaction)
    print(f"Produced: {transaction}")
    time.sleep(1)