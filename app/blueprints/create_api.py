import json

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

create = Blueprint('create', __name__)


@create.route('/create/alias', methods=['POST'], strict_slashes=False)
@login_required
def create_alias():
    data = json.loads(request.data.decode())
    alias = data['alias']
    fee = float(data['fee']) * (10 ** 8)
    data = current_user.wallet.createAlias(alias, txFee=int(fee))
    return jsonify(data)
