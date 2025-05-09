import random
import re

from faker import Faker

fake = Faker()

def generate_random_user_for_registration():
    """
    Generate random user details for registration.
    Returns Random user details for registration.
    """
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

def generate_random_details_for_pay_bill(amount):
    """
    Generate random user details for pay bill.
    Returns Random user details for pay bill.
    """
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

def convert_to_float_2dp(value):
    """
    Converts an int to a float with 2 decimal points as a string.
    If value is already a float, return it as a string with 2 decimal places.
    """
    if isinstance(value, int):
        return f"{float(value):.2f}"
    elif isinstance(value, float):
        return f"{value:.2f}"
    else:
        raise ValueError("Input must be an int or float.")