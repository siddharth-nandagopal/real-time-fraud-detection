from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'fraud-alerts',
    bootstrap_servers='kafka01:29192,kafka02:29292,kafka03:29392',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    alert = {
        'transaction_id': transaction['transaction_id'],
        'user_id': transaction['user_id'],
        'amount': transaction['amount'],
        'timestamp': transaction['timestamp'],
        'alert': 'Fraudulent transaction detected!'
    }
    print(f"Handle the Fraud Alert: {alert}")