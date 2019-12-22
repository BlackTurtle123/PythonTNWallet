import requests
from flask import Blueprint

from app.network_settings import get_pywaves
from app.utils import address_data_regex

data = Blueprint('data', __name__)


@data.route('/address/data/<addr>')
def address_data(addr):
    r = requests.get(get_pywaves().NODE + "/addresses/data/" + addr)
    return r.content.decode()


@data.route('/data/<addr>/regex/<regex>')
def addr_data_regex(addr, regex):
    return address_data_regex(addr, regex)
