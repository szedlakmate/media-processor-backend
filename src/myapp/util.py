import random
import string


def generate_random_string(length=10):
    # printing letters
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
