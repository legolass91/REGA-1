import random
import string
from faker import Faker


def generate_login():
    login = ''.join(random.choices(string.ascii_letters + string.digits, k=10)).lower()
    return login + str(random.randint(1970, 2001))


def generate_password():
    first_char = random.choice(string.ascii_letters)
    rest_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    password = first_char + rest_chars
    return password


def generate_first_name():
    fake = Faker()
    f_name = fake.first_name()
    return f_name.lower()


generate_first_name()


def generate_last_name():
    fake = Faker()
    l_name = fake.last_name()
    return l_name.lower()



