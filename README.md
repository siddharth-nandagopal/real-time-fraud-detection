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
7. Start [fraud_api](https://github.com/siddharth-nandagopal/real-time-fraud-detection/tree/development/fraud_api)
	```
	python3 main.py
	```
	GET http://127.0.0.1:8000/alerts
8. Run test:
	```
	python3 -m unittest tests.test_alert
	```
	(OR)
	```
	pytest tests.test_alert
	```
	

# TODO
react UI to display alerts
ML?


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





### Issues:
```
Because no versions of fastapi match >0.115.0,<0.116.0
 and fastapi (0.115.0) depends on starlette (>=0.37.2,<0.39.0), fastapi (>=0.115.0,<0.116.0) requires starlette (>=0.37.2,<0.39.0).
So, because real-time-fraud-detection depends on both starlette (^0.39.2) and fastapi (^0.115.0), version solving failed.
```
#### Solution:
set the starlette version to be >=0.37.2 and <0.39.0, which is 0.38.6
set the fastapi version to be >=0.115.0 and <0.116.0


### Issues:
```
Traceback (most recent call last):
  File "/real-time-fraud-detection/fraud_api/main.py", line 3, in <module>
    from app import app
  File "/real-time-fraud-detection/fraud_api/app/__init__.py", line 5, in <module>
    from app.routers import FraudRouter
  File "/real-time-fraud-detection/fraud_api/app/routers/FraudRouter.py", line 4, in <module>
    from app.controllers.FraudController import FraudController as controller
```
#### Solution:
naming convention - 
1. Modules should have short, all-lowercase names.  Underscores can be used in the module name if it improves readability.  Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.
2. Name of the file that defines the model shall be all lowercase (eg: alert.py). It must match the name of the <Prefix>Controller (eg: AlertController.py). It must match the name of the file that deines the routers and all lowercase (eg: alerts.py).
3. Each directory that holds files that are used as a modules elsewhere, must have '__init__.py' file.
4. Almost without exception, class names use the CapWords convention. Classes for internal use have a leading underscore in addition.
References:
1. https://w3.cs.jmu.edu/spragunr/CS240_F12/style_guide.shtml#:~:text=Package%20and%20Module%20Names%20Modules,use%20of%20underscores%20is%20discouraged.
2. https://medium.com/@leeli0830/8-python-naming-convention-you-must-know-bbab94735b93
3. https://discuss.python.org/t/how-exactly-does-init-py-influence-module-search-order/24759 



### Issue:
Connects to mongodb using mongoengine, still returns empty list
#### Solution: 
set 'collection' property inside 'meta' attribute in the model definition


### Issue:
Object of type Alert is not JSON serializable
#### Solution:
application is larger or you have more complex objects, consider using a serialization library like marshmallow or pydantic
(OR)
queryset.to_json()


### Issue:
```
Traceback (most recent call last):
  File "/real-time-fraud-detection/fraud_api/tests/test_alert.py", line 9, in <module>
    from app import app
ModuleNotFoundError: No module named 'app'
```

Module Execution: Note that if you run test_alert.py directly, you might encounter an import error due to how relative imports work. To execute the script properly, you can run it from the top level of your project.

```
Traceback (most recent call last):
  File "/real-time-fraud-detection/fraud_api/tests/test_alert.py", line 9, in <module>
    from ..app import app
ImportError: attempted relative import with no known parent package
```
#### Solution:
To execute the script properly, you can run it from the top level of your project.
To run test_alert.py, navigate to the fraud_api directory and execute:
```
python3 -m tests.test_alert
```


### Issue:
```
E
======================================================================
ERROR: setUpClass (tests.test_alert.TestAlert)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/real-time-fraud-detection/fraud_api/tests/test_alert.py", line 31, in setUpClass
    connect('mongoenginetest', host='mongomock://localhost/mocking_db')
  File "/.asdf/installs/python/3.12.0/lib/python3.12/site-packages/mongoengine/connection.py", line 469, in connect
    register_connection(alias, db, **kwargs)
  File "/.asdf/installs/python/3.12.0/lib/python3.12/site-packages/mongoengine/connection.py", line 253, in register_connection
    conn_settings = _get_connection_settings(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/.asdf/installs/python/3.12.0/lib/python3.12/site-packages/mongoengine/connection.py", line 120, in _get_connection_settings
    raise Exception(
Exception: Use of mongomock:// URI or 'is_mock' were removed in favor of 'mongo_client_class=mongomock.MongoClient'. Check the CHANGELOG for more info

----------------------------------------------------------------------
Ran 0 tests in 0.001s

FAILED (errors=1)
```
The error message indicates that there is an issue with how one is trying to connect to a mocked MongoDB instance using mongomock in one's tests. The mongomock:// URI is no longer supported in the version of mongoengine one is using.
#### Solution:
One need to use mongo_client_class=mongomock.MongoClient in one's connection settings. Here's how one can adjust one's setUpClass method:
```
# Connect to the mock database
connect('mongoenginetest', mongo_client_class=MongoClient)
```