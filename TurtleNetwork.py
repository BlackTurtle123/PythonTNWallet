import json
import sys

import requests
from flask import Flask, request, url_for, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, current_user

from app import network_settings as nset
from app.blueprints.gateway_api import gateway_api
from app.blueprints.html import html
from app.blueprints.data_api import data
from app.blueprints.tickers_api import tickers
from app.models.User import User
from app.network_settings import get_pywaves, set_gateways
from app.utils.free_port import get_free_port
from app.utils.gateway_list import create_gateway_list
from app.utils.resource_path import resource_path

if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.register_blueprint(tickers)
app.register_blueprint(data)
app.register_blueprint(html)
app.register_blueprint(gateway_api)
app.secret_key = "TurtleNetwork"


@app.context_processor
def inject_network_and_currency_and_base_fee():
    return dict(network=nset.get_network(), currency=get_pywaves().DEFAULT_CURRENCY,
                base_fee=get_pywaves().DEFAULT_TX_FEE)


nset.set_network("mainnet")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'html.login'


@login_manager.user_loader
def load_user(seed):
    return User(seed)


@app.route('/assets/burn/<asset>', methods=['POST'], strict_slashes=False)
@login_required
def burn_asset(asset):
    py_asset = get_pywaves().Asset(assetId=asset)
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** py_asset.decimals)
    fee = float(data['fee']) * (10 ** 8)
    burn = current_user.wallet.burnAsset(py_asset, int(amount), txFee=int(fee))
    return jsonify(burn)


@app.route('/tn/send/', methods=['POST'], strict_slashes=False)
@login_required
def send_tn():
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** 8)
    recipient = data['addr']
    attachment = data['attachment']
    fee = float(data['fee']) * (10 ** 8)
    alias = json.loads(active_alias(recipient))
    try:
        if 'address' not in alias:
            send = current_user.wallet.sendWaves(get_pywaves().Address(address=recipient), int(amount),
                                                 attachment=attachment,
                                                 txFee=int(fee))
        else:
            send = current_user.wallet.sendWaves(get_pywaves().Address(address=alias['address']), int(amount),
                                                 attachment=attachment,
                                                 txFee=int(fee))
        return jsonify(send)
    except (get_pywaves().PyWavesException, ValueError) as e:
        return jsonify(str(e))


@app.route('/assets/send/<asset>', methods=['POST'], strict_slashes=False)
@login_required
def send_asset(asset):
    py_asset = get_pywaves().Asset(assetId=asset)
    data = json.loads(request.data.decode())
    addr = data['addr']
    amount = float(data['amount']) * (10 ** py_asset.decimals)
    fee = float(data['fee']) * (10 ** 8)
    alias = json.loads(active_alias(addr))
    try:
        if 'address' not in alias:
            send = current_user.wallet.sendAsset(get_pywaves().Address(addr), py_asset, int(amount), txFee=int(fee))
        else:
            send = current_user.wallet.sendAsset(get_pywaves().Address(alias['address']), py_asset, int(amount),
                                                 txFee=int(fee))

        return jsonify(send)
    except (get_pywaves().PyWavesException, ValueError) as e:
        return jsonify(str(e))


@app.route('/create/alias', methods=['POST'], strict_slashes=False)
@login_required
def create_alias():
    data = json.loads(request.data.decode())
    alias = data['alias']
    fee = float(data['fee']) * (10 ** 8)
    data = current_user.wallet.createAlias(alias, txFee=int(fee))
    return jsonify(data)


@app.route('/state/aliases/by-address/<addr>')
def active_alias_by_addr(addr):
    r = requests.get(get_pywaves().NODE + "/alias/by-address/" + addr)
    return r.content.decode()


@app.route('/state/aliases/by-alias/<alias>')
def active_alias(alias):
    r = requests.get(get_pywaves().NODE + "/alias/by-alias/" + alias)
    return r.content.decode()


@app.route('/state/leases/<addr>')
def active_leasing(addr):
    r = requests.get(get_pywaves().NODE + "/leasing/active/" + addr)
    return r.content.decode()


@app.route('/state/leases/cancel/<id>')
@login_required
def cancel_active_leasing(id):
    send = current_user.wallet.leaseCancel(leaseId=id, txFee=get_pywaves().DEFAULT_TX_FEE)
    return jsonify(send)


@app.route('/state/leases/start', methods=['POST'], strict_slashes=False)
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


@app.route('/state/transactions/<addr>/<amount>')
def history_tx(addr, amount):
    r = requests.get(get_pywaves().NODE + "/transactions/address/" + addr + "/limit/" + amount)
    return r.content.decode()


@app.route('/login', methods=['POST'], strict_slashes=False)
def do_admin_login():
    data = request.form
    seed = data['seed']
    pk = data['pk']
    nset.set_network(data['network'])
    login_user(User(pk, seed))
    if nset.get_network() == 'mainnet':
        set_gateways(create_gateway_list())

    return redirect(url_for('html.home'))


PORT = get_free_port()
PYWAVES = get_pywaves()


def run_server():
    app.run(host='127.0.0.1', port=PORT, threaded=True)


if __name__ == '__main__':
    run_server()

    # init_gui(app, window_title="Turtle Network Wallet", icon="static/favicon.ico")
