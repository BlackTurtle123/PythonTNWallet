import requests
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
import json

from app.models.Token import Token
from app.network_settings import get_pywaves, set_gateways, get_gateways

html = Blueprint('html', __name__)


@html.route('/portfolio')
@login_required
def portfolio():
    result = requests.get(get_pywaves().NODE + '/assets/balance/' + current_user.wallet.address)
    balances = json.loads(result.content)['balances']
    portfolio = []
    for balance in balances:
        asset = Token(balance['issueTransaction']['id'], balance['issueTransaction']['decimals'],
                      balance['balance'], balance['issueTransaction']['sender'],
                      balance['issueTransaction']['name'], balance['issueTransaction']['description'])
        portfolio.append(asset)
    return render_template('portfolio.html', portfolio=portfolio)


@html.route('/details/<assetid>', strict_slashes=False)
@login_required
def details_asset(assetid):
    asset_details = get_pywaves().Asset(assetId=assetid)
    if asset_details.decimals == 0:
        asset_balance = current_user.wallet.balance(assetId=assetid)
    else:
        asset_balance = current_user.wallet.balance(assetId=assetid) / (10 ** asset_details.decimals)
    asset_smart = asset_details.isSmart()
    return render_template('details.html', asset_details=asset_details, asset_balance=asset_balance,
                           asset_smart=asset_smart, extra_fees=current_user.extra_fees)


@html.route('/dex')
@login_required
def dex_overview():
    return render_template('dex.html')


@html.route('/alias')
@login_required
def alias_overview():
    return render_template('alias.html', address=current_user.wallet.address, extra_fees=current_user.extra_fees)


@html.route('/data')
@login_required
def data_overview():
    return render_template('data_transfer.html', address=current_user.wallet.address, extra_fees=current_user.extra_fees)


@html.route('/asset/create')
@login_required
def asset_create():
    return render_template('asset_create.html')


@html.route('/explorer')
@login_required
def explorer():
    return render_template('explorer.html')


@html.route('/lease/overview')
@login_required
def lease_overview():
    return render_template('lease.html', address=current_user.wallet.address, extra_fees=current_user.extra_fees)


@html.route('/')
@login_required
def home():
    return render_template('home.html', address=current_user.wallet.address,
                           balance=float(current_user.wallet.balance()) / 10 ** 8,
                           extra_fees=current_user.extra_fees / 10 ** 8)


@html.route('/login', methods=['GET'], strict_slashes=False)
def login():
    return render_template('login.html')


@html.route('/logout', methods=['GET'], strict_slashes=False)
@login_required
def do_logout():
    logout_user()
    set_gateways([])
    return redirect(url_for('html.login'))



@html.route('/gateway/overview')
@login_required
def gateways_overview():
    return render_template('gateways.html', gateways=get_gateways(), extra_fees=current_user.extra_fees,
                           address=current_user.wallet.address)
