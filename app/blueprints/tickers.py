from flask import Blueprint

from app import network_settings as nset
from app.utils.address_data_regex import address_data_regex

tickers = Blueprint('tickers', __name__)


@tickers.route('/tickers')
def data_tickers(regex='^ticker_.*$'):
    return address_data_regex(nset.get_network, regex)


@tickers.route('/tickers/<assetid>')
def data_tickers_by_asset_id(assetid):
    return address_data_regex(nset.get_network, '^ticker_<' + assetid + '>')


@tickers.route('/tickers/status')
def data_tickers_status(regex='^status_.*$'):
    return address_data_regex(nset.get_network, regex)


@tickers.route('/tickers/status/<assetid>')
def data_tickers_status_by_asset_id(assetid):
    return address_data_regex(nset.get_network, '^status_<' + assetid + '>')


@tickers.route('/tickers/email')
def data_tickers_email(regex='^email_.*$'):
    return address_data_regex(nset.get_network, regex)


@tickers.route('/tickers/email/<assetid>')
def data_tickers_email_by_asset_id(assetid):
    return address_data_regex(nset.get_network, '^email_<' + assetid + '>')
