import random
import re

from faker import Faker

fake = Faker()

#Generate random user details for registration
def generate_random_user_for_registration():
    name = fake.first_name().lower()
    number = random.randint(10000, 99999)

    return {
        'fname': fake.first_name(),
        'lname': fake.last_name(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zipcode': str(random.randint(100000, 999999)),
        'phone': str(random.randint(6000000000, 9999999999)),
        'ssn': str(random.randint(1000, 9999)),
        'uname': name + str(number),
        'pwd': "Test@123",
        'pwd1': "Test@123",
    }

    # Generate random user details for registration
def generate_random_details_for_pay_bill(amount):
    return {
        'name': fake.first_name(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zipcode': str(random.randint(100000, 999999)),
        'phone': str(random.randint(6000000000, 9999999999)),
        'account': str(random.randint(1000, 9999)),
        'amount': amount
    }

def compare_currency_with_number(value1, value2):
    """
    Compare a currency-formatted string
    Returns True if they are equal after conversion, else False.
    """
    def normalize(value):
        if isinstance(value, str):
            value = re.sub(r'[^0-9.]', '', value)  # Remove non-numeric characters except '.'
        return float(value)

    return round(normalize(value1), 2) == round(normalize(value2), 2)

