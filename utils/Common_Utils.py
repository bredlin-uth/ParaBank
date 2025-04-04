import random
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
