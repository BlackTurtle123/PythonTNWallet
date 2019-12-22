from flask import Blueprint, request, redirect, url_for
from flask_login import login_user
from app import network_settings as nset
from app.models.User import User
from app.network_settings import set_gateways
from app.utils import create_gateway_list

login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'], strict_slashes=False)
def do_admin_login():
    data = request.form
    seed = data['seed']
    pk = data['pk']
    nset.set_network(data['network'])
    login_user(User(pk, seed))
    if nset.get_network() == 'mainnet':
        set_gateways(create_gateway_list())

    return redirect(url_for('html.home'))
