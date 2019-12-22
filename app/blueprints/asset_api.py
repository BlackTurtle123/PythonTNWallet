from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.network_settings import get_pywaves
import json

from app.utils import active_alias

asset = Blueprint('asset', __name__)


@asset.route('/assets/burn/<asset>', methods=['POST'], strict_slashes=False)
@login_required
def burn_asset(asset):
    py_asset = get_pywaves().Asset(assetId=asset)
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** py_asset.decimals)
    fee = float(data['fee']) * (10 ** 8)
    burn = current_user.wallet.burnAsset(py_asset, int(amount), txFee=int(fee))
    return jsonify(burn)


@asset.route('/assets/send/<asset>', methods=['POST'], strict_slashes=False)
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
