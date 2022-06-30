import random
import string

def get_random_token(length):
    # With combination of lower and digits
    characters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str
