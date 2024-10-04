from kafka import KafkaConsumer
import json
from pymongo import MongoClient

MONGO_URI = "mongodb://mongo1:27017/"
DB_NAME = "fraud_database"
COLLECTION_NAME = "fraud_alert_collection"

consumer = KafkaConsumer(
    'fraud-alerts',
    bootstrap_servers='kafka01:29192,kafka02:29292,kafka03:29392',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    # auto_offset_reset='earliest', # The auto_offset_reset property is set to earliest to ensure that the consumer starts from the earliest message in the topic.
    # enable_auto_commit=False # The enable_auto_commit property is set to False to prevent the consumer from automatically committing the offset after processing a message.
)

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database
db = client[DB_NAME]

# Access the collection
collection = db[COLLECTION_NAME]


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

    # Insert the JSON record into the collection
    result = collection.insert_one(alert)

    # Print the ID of the inserted document
    print(f"Inserted alert -> document ID: {result.inserted_id}")

# Close the connection
client.close()






# We can then use the subscribe method to subscribe to one or more topics.
# # Subscribe to a specific topic
# consumer.subscribe(topics=['my-topic'])

# Finally, we can use the poll method to poll for new data and process it as required.
# # Poll for new messages
# while True:
#     msg = consumer.poll(timeout_ms=1000)
#     if msg:
#         for topic, partition, offset, key, value in msg.items():
#             print("Topic: {} | Partition: {} | Offset: {} | Key: {} | Value: {}".format(
#                 topic, partition, offset, key, value.decode("utf-8")
#             ))
#     else:
#         print("No new messages")