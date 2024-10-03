from faker import Faker
import random
import sys

fake = Faker()

def generate_transaction():
    return {
        "transaction_id": random.randint(1000, 9999),
        "timestamp": fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": random.randint(1, 100),
        "card_number": fake.credit_card_number(),
        "amount": round(random.uniform(1, 10000), 2)
    }
