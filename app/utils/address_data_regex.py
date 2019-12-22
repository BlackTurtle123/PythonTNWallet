import requests

from app.network_settings import get_pywaves


def address_data_regex(addr, regex):
    r = requests.get(get_pywaves().NODE + "/addresses/data/" + addr + "?matches=" + regex)
    return r.content.decode()
