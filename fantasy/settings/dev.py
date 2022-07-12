from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ax&p%k515c1ql8))0mg*q46-1-2(mo_j3++7r(ux7j$98uxqkb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["my-fantasy-team.herokuapp.com", "127.0.0.1"]