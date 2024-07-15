from datetime import timedelta
import random
import string


characters = string.ascii_letters + string.digits + string.punctuation
random_string1 = ''.join(random.choice(characters) for _ in range(25))
random_string2 = ''.join(random.choice(characters) for _ in range(25))


class Configuration:
    JWT_COOkIE_SECURE = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = random_string1
    SECRET_KEY = random_string2  
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=72)
    SESSION_COOKIE_SAMESITE = 'None'