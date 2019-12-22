from flask import Blueprint
import json
from app import network_settings as nset
from app.models.Verification import Verification
from app.utils.address_data_regex import address_data_regex

tickers = Blueprint('tickers', __name__)


@tickers.route('/tickers')
def data_tickers(regex='^ticker_.*$'):
    return address_data_regex(nset.TICKER_ORACLE, regex)


@tickers.route('/tickers/<assetid>')
def data_tickers_by_asset_id(assetid):
    return address_data_regex(nset.TICKER_ORACLE, '^ticker_<' + assetid + '>')


@tickers.route('/tickers/status')
def data_tickers_status(regex='^status_.*$'):
    return address_data_regex(nset.TICKER_ORACLE, regex)


@tickers.route('/tickers/status/<assetid>')
def data_tickers_status_by_asset_id(assetid):
    return address_data_regex(nset.TICKER_ORACLE, '^status_<' + assetid + '>')


@tickers.route('/tickers/email')
def data_tickers_email(regex='^email_.*$'):
    return address_data_regex(nset.TICKER_ORACLE, regex)


@tickers.route('/tickers/email/<assetid>')
def data_tickers_email_by_asset_id(assetid):
    return address_data_regex(nset.TICKER_ORACLE, '^email_<' + assetid + '>')


@tickers.route("/tickers/<assetid>/full")
def data_full_ticker_info_asset(assetid):
    try:
        ticker = json.loads(data_tickers_by_asset_id(assetid))[0]['value']
        status = json.loads(data_tickers_status_by_asset_id(assetid))[0]['value']
        email = json.loads(data_tickers_email_by_asset_id(assetid))[0]['value']
        verifcation = Verification(assetid, ticker, status, email)
    except IndexError:
        verifcation = Verification(assetid)
    return json.dumps(verifcation.__dict__)
