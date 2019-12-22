import configparser

import pywaves as py

py.DEFAULT_TX_FEE = 2000000
TICKER_ORACLE = '3Ji18p2UzvemqKe6Npn3qZUAve1Vs4rkZDP'
NETWORK = 'mainnet'


def set_network_settings(network):
    config = configparser.ConfigParser()
    config.read('network.cfg')
    network = network.upper()
    NODE = config[network]['NODE']
    set_ticker_oracle(config[network]['TICKER_ORACLE'])
    py.DEFAULT_TX_FEE = int(config[network]['FEE'])
    py.setNode(NODE, network + config[network]['CURRENCY'], config[network]['CHAR'])
    py.setMatcher(config[network]['MATCHER'])
    py.setDatafeed(config[network]['DATA_FEED'])
    py.DEFAULT_CURRENCY = config[network]['CURRENCY']
    py.THROW_EXCEPTION_ON_ERROR = config['GENERAL'].getboolean('THROW_ERRORS')


def set_network(network):
    global NETWORK
    NETWORK = network
    set_network_settings(NETWORK)


def set_ticker_oracle(oracle):
    global TICKER_ORACLE
    TICKER_ORACLE = oracle


def get_network():
    return NETWORK


def get_ticker_oracle():
    return TICKER_ORACLE


def get_pywaves():
    return py
