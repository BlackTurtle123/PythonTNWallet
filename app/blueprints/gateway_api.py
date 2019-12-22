import requests
from flask import request, jsonify, Blueprint, current_app
from flask_login import login_required, current_user

from app.models import Gateway
from app.network_settings import get_pywaves, get_gateways, set_gateways
import json

gateway_api = Blueprint('gateway_api', __name__)


def get_addr_gateway(url, addr):
    r = requests.get("https://" + url + ".blackturtle.eu/api/v1/coin-address/" + addr)
    return r.content.decode()


@gateway_api.route('/gateway/<gateway>')
@login_required
def gateways_detail(gateway):
    gw: Gateway = next((x for x in get_gateways() if x.name.lower() == gateway.lower()), None)
    index = get_gateways().index(gw)
    gw.set_personal_wallet(get_addr_gateway(gw.url, current_user.wallet.address))
    current_app.logger.info(get_gateways())

    new_gw_list = get_gateways()
    new_gw_list[index] = gw
    set_gateways(new_gw_list)
    current_app.logger.info(get_gateways())

    return json.dumps(gw.__dict__)


@gateway_api.route('/gw/send/tn', methods=['POST'], strict_slashes=False)
@login_required
def gw_send_tn():
    data = request.data
    json_data = json.loads(data.decode())
    dest = json_data['addr']
    amount = float(json_data['amount']) * (10 ** 8)
    fee = float(json_data['fee']) * (10 ** 8)
    gateway = get_pywaves().Address(address=get_addr_gateway('gateway', dest))
    try:
        result = current_user.wallet.sendWaves(gateway, int(amount), txFee=int(fee))
        return jsonify(result)
    except (get_pywaves().PyWavesException, ValueError) as e:
        return jsonify(str(e))


@gateway_api.route('/gw/send/<gateway>', methods=['POST'], strict_slashes=False)
@login_required
def gw_send_currencie(gateway):
    gw: Gateway = next((x for x in get_gateways() if x.name.lower() == gateway.lower()), None)
    data = request.data
    gateway = get_pywaves().Address(address=gw.general_addr)
    json_data = json.loads(data.decode())
    dest = json_data['addr']
    amount = float(json_data['amount']) * (10 ** 8)
    fee = float(json_data['fee']) * (10 ** 8)
    result = current_user.wallet.sendAsset(gateway, get_pywaves().Asset(gw.asset_id), int(amount), txFee=int(fee),
                                           attachment=dest)
    return jsonify(result)
