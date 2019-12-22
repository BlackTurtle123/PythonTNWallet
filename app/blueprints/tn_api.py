from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import json

from app.network_settings import get_pywaves
from app.utils import active_alias

tn = Blueprint('tn', __name__)


@tn.route('/tn/send/', methods=['POST'], strict_slashes=False)
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
