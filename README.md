# Real-Time Fraud Detection with Apache Kafka

In today's financial environment, real-time fraud detection is vital for secure payment processing. Apache Kafka, known for its high throughput and low latency, is an excellent tool for building a fraud detection system. This guide will lead you through the steps to set up a real-time fraud detection system using Kafka, from installation to implementation.

## Objective
The goal is to identify potentially fraudulent transactions as they occur by analyzing payment data in real time.

# Getting Started

1. Make sure to start [kafka cluster](https://github.com/siddharth-nandagopal/kafka-kraft-cluster)
2. Create kafka topic
	Create a topic for payment transactions
	```
	~bin/> kafka-topics --create --topic payment-transactions --bootstrap-server kafka01:9092 --partitions 3 --replication-factor 3
	```
	Create a topic for fraud alerts
	```
	~bin/> kafka-topics --create --topic fraud-alerts --bootstrap-server kafka01:9092 --partitions 3 --replication-factor 3
	```
3. Install dependencies
	```
	asdf install

	poetry install
	```
4. Start [transaction_producer](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/transaction_producer)
	```
	python3 transaction_producer.py 
	```
5. Start [fraud_detector](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/fraud_detector)
	```
	python3 fraud_detector.py 
	```
6. Start [fraud_handler](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/fraud_handler)
	```
	python3 fraud_handler.py 
	```




# Troubleshoot guide/frequent issues

### Issue:
```
Traceback (most recent call last):
  File "/real-time-fraud-detection/transaction_producer/transaction_producer.py", line 1, in <module>
    from kafka import KafkaProducer
  File ".asdf/installs/python/3.12.0/lib/python3.12/site-packages/kafka/__init__.py", line 21, in <module>
    from kafka.consumer import KafkaConsumer
  File ".asdf/installs/python/3.12.0/lib/python3.12/site-packages/kafka/consumer/__init__.py", line 3, in <module>
    from .simple import SimpleConsumer
  File ".asdf/installs/python/3.12.0/lib/python3.12/site-packages/kafka/consumer/simple.py", line 13, in <module>
    from kafka.vendor.six.moves import queue # pylint: disable=import-error
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'kafka.vendor.six.moves'
```
#### Solution:
```
pip install kafka-python-ng
```
(or)
```
poetry add --group=main kafka-python-ng
```
refer: https://github.com/dpkp/kafka-python/issues/2412#issuecomment-2030459360