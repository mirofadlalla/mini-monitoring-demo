import random
import string

DATABASE = {}


def generate_code(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits

    while True:
        code = "".join(random.choices(alphabet, k=length))

        if code not in DATABASE:
            return code