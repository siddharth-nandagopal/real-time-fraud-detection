from kafka import KafkaConsumer, KafkaProducer
import json

def is_fraudulent(transaction):
    # Simple rule: flag transactions over $500 as fraudulent
    return transaction['amount'] > 500

consumer = KafkaConsumer(
    'payment-transactions',
    bootstrap_servers='kafka01:29192,kafka02:29292,kafka03:29392',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='kafka01:29192,kafka02:29292,kafka03:29392',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for message in consumer:
    transaction = message.value
    if is_fraudulent(transaction):
        alert = {
            'transaction_id': transaction['transaction_id'],
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'timestamp': transaction['timestamp'],
            'alert': 'Fraudulent transaction detected!'
        }
    producer.send('fraud-alerts', value=alert)
    print(f"Fraud Alert: {alert}")