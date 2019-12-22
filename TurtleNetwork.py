import sys

from flask import Flask
from flask_login import LoginManager

from app import network_settings as nset
from app.blueprints import asset, gateway_api, html, data, login, state, tickers, tn, create
from app.models.User import User
from app.network_settings import get_pywaves
from app.utils import get_free_port, resource_path

if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.register_blueprint(asset)
app.register_blueprint(create)
app.register_blueprint(data)
app.register_blueprint(gateway_api)
app.register_blueprint(html)
app.register_blueprint(login)
app.register_blueprint(state)
app.register_blueprint(tickers)
app.register_blueprint(tn)

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


PORT = get_free_port()
PYWAVES = get_pywaves()


def run_server():
    app.run(host='127.0.0.1', port=PORT, threaded=True)


if __name__ == '__main__':
    run_server()

    # init_gui(app, window_title="Turtle Network Wallet", icon="static/favicon.ico")
