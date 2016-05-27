import string

import random

ALPHANUMERIC = string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_random_string(length=40):
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(ALPHANUMERIC) for _ in range(length))
