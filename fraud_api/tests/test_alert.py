from unittest import TestCase

import json
import datetime
from bson import ObjectId

from mongoengine import connect, disconnect
from mongoengine.errors import InvalidQueryError, LookUpError
from mongomock import MongoClient
from starlette.testclient import TestClient

from app import app
from app.models.alert import Alert

"""
    Initialize the Test Client so that FastAPI runs without needing to be started with uvicorn.
"""
client = TestClient(app)


class TestAlert(TestCase):

    @classmethod
    def setUpClass(cls):
        """
            The setUp function is the same as init where the test file is run for the first time.
        """
        disconnect()

        """
            useful to plug MongoEngine to alternative implementations (mongomock, montydb, mongita, etc).
            mongomock is historically the one suggested for MongoEngine and is a package to do just what the name implies, mocking a mongo database.
        """
        # connect('mongoenginetest', host='mongomock://localhost/mocking_db')
        # Connect to the mock database
        connect('mongoenginetest', mongo_client_class=MongoClient)

    @classmethod
    def tearDownClass(cls):
        """
            The tearDown function will be executed when all tests have been completed.
        """
        disconnect()

    def setUp(self):
        # This will run before each test
        Alert.drop_collection()  # Clear the collection before each test

    def test_get_api_notfound(self):
        response = client.get("/alerts-not-found")
        assert response.status_code == 404
    
    def test_get_alerts_api_single_record(self):
        # Create single mock record
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()

        response = client.get("/alerts")

        res = response.json()
        res = json.loads(res['values'])
        print(f"Fraud Alert Test response: {res}")
        transaction_id = res[0]['transaction_id']

        assert response.status_code == 200

        alert = Alert.objects(transaction_id=transaction_id).first()
        assert alert.transaction_id == transaction_id
        
    def test_get_alerts_api_multiple_records(self):
        # Create multiple mock records
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        alert2 = Alert(transaction_id=2, user_id=2, alert="mock alert 2", amount=2000.32, timestamp=datetime.datetime.now())
        alert2.save()

        response = client.get("/alerts")

        res = response.json()
        res = json.loads(res['values'])
        print(f"Fraud Alert Test response: {res}")
        transaction_id = res[0]['transaction_id']

        assert response.status_code == 200

        alert = Alert.objects(transaction_id=transaction_id).first()
        assert alert.transaction_id == transaction_id

    def test_get_alerts_empty(self):
        # Test retrieving alerts when none exist
        retrieved_alerts = Alert.objects()
        self.assertEqual(retrieved_alerts.count(), 0)

    def test_get_alerts_single(self):
        # Test retrieving a single alert
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        
        retrieved_alerts = Alert.objects()
        self.assertEqual(retrieved_alerts.count(), 1)
        self.assertEqual(retrieved_alerts[0].alert, "mock alert 1")

    def test_get_alerts_multiple(self):
        # Test retrieving multiple alerts
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        alert2 = Alert(transaction_id=2, user_id=2, alert="mock alert 2", amount=2000.32, timestamp=datetime.datetime.now())
        alert2.save()
        
        retrieved_alerts = Alert.objects()
        self.assertEqual(retrieved_alerts.count(), 2)
        self.assertIn(alert1, retrieved_alerts)
        self.assertIn(alert2, retrieved_alerts)

    def test_get_alerts_with_specific_filter(self):
        # Test retrieving alerts with a specific filter
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        alert2 = Alert(transaction_id=2, user_id=1, alert="mock alert 2", amount=2000.32, timestamp=datetime.datetime.now())
        alert2.save()

        # Filter to retrieve the second alert
        retrieved_alerts = Alert.objects(transaction_id=2)
        self.assertEqual(retrieved_alerts.count(), 1)
        self.assertEqual(retrieved_alerts[0].alert, "mock alert 2")

    def test_get_alerts_nonexistent_filter(self):
        # Test retrieving alerts with a filter that doesn't match
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        
        # Attempt to retrieve alerts with a non-existent transaction_id
        retrieved_alerts = Alert.objects(transaction_id=0)
        self.assertEqual(retrieved_alerts.count(), 0)

    def test_get_alerts_check_ids(self):
        # Test that the retrieved alerts maintain their transaction_ids
        alert1 = Alert(transaction_id=1, user_id=1, alert="mock alert 1", amount=1000.32, timestamp=datetime.datetime.now())
        alert1.save()
        alert2 = Alert(transaction_id=2, user_id=1, alert="mock alert 2", amount=2000.32, timestamp=datetime.datetime.now())
        alert2.save()

        retrieved_alerts = Alert.objects()
        # order by -timestamp (descending)
        self.assertEqual(retrieved_alerts[0].user_id, alert2.user_id)
        self.assertEqual(retrieved_alerts[1].user_id, alert1.user_id)