import requests

from app.network_settings import get_pywaves


def active_alias(alias):
    r = requests.get(get_pywaves().NODE + "/alias/by-alias/" + alias)
    return r.content.decode()
