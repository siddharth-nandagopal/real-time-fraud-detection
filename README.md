
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
3. Start [transaction_producer](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/transaction_producer)
4. Make sure to start [fraud_detector](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/fraud_detector)