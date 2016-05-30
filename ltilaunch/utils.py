import re
import string

import random
from django.contrib.sites.shortcuts import get_current_site

ALPHANUMERIC = string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_random_string(length=40):
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(ALPHANUMERIC) for _ in range(length))


def absolute_url_for_path(request, path):
    site = get_current_site(request)
    return "http://{domain}{path}".format(
        domain=site.domain,
        path=path)


def as_https(url):
    return re.sub(r"^http:", "https:", url)
