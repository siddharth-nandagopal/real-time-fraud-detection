from mongoengine import *


class Alert(Document):
    transaction_id = IntField(min_value=None, max_value=None, required=True)
    user_id = IntField(min_value=1, max_value=100, required=True)
    alert = StringField(max_length=40, required=True)
    amount = DecimalField(min_value=1, max_value=10000, force_string=False, precision=2, rounding='ROUND_HALF_UP')
    timestamp = DateTimeField(required=True)

    meta = {
        'collection': 'fraud_alert_collection',
        'ordering': ['-timestamp'],
        'indexes': [
            {'fields': ['transaction_id'], 'expireAfterSeconds': 3600},
            {'fields': ['user_id'], 'expireAfterSeconds': 3600}
        ]
    }
