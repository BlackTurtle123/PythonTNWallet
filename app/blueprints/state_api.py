import requests
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.network_settings import get_pywaves
import json

from app.utils.active_alias import active_alias

state = Blueprint('state', __name__)


@state.route('/state/aliases/by-address/<addr>')
def active_alias_by_addr(addr):
    r = requests.get(get_pywaves().NODE + "/alias/by-address/" + addr)
    return r.content.decode()


@state.route('/state/aliases/by-alias/<alias>')
def active_alias_by_alias(alias):
    return active_alias(alias)


@state.route('/state/leases/<addr>')
def active_leasing(addr):
    r = requests.get(get_pywaves().NODE + "/leasing/active/" + addr)
    return r.content.decode()


@state.route('/state/leases/cancel/<id>')
@login_required
def cancel_active_leasing(id):
    send = current_user.wallet.leaseCancel(leaseId=id, txFee=get_pywaves().DEFAULT_TX_FEE)
    return jsonify(send)


@state.route('/state/leases/start', methods=['POST'], strict_slashes=False)
@login_required
def start_leasing():
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** 8)
    recipient = data['addr']
    alias = json.loads(active_alias(recipient))
    if 'address' not in alias:
        send = current_user.wallet.lease(get_pywaves().Address(address=recipient), int(amount),
                                         txFee=get_pywaves().DEFAULT_TX_FEE)
    else:
        send = current_user.wallet.lease(get_pywaves().Address(address=alias['address']), int(amount),
                                         txFee=get_pywaves().DEFAULT_TX_FEE)
    return jsonify(send)


@state.route('/state/transactions/<addr>/<amount>')
def history_tx(addr, amount):
    r = requests.get(get_pywaves().NODE + "/transactions/address/" + addr + "/limit/" + amount)
    return r.content.decode()
