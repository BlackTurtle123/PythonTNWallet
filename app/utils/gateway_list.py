from app.models.Gateway import Gateway


def create_gateway_list(network="mainnet"):
    if network != "mainnet":
        return []
    gateways = [Gateway('----------', '3JbpUeiV6BN9k2cMccKE5LZrrQ8wN44pxWy',
                        0.01, 'Waves', 'EzwaF58ssALcUCZ9FbyeD1GTSteoZAQZEDTqBAXHfq8y', 'wavesgateway', 'wB-bg-WAV.png'),
                Gateway('----------', '3JnNnw91XQr3pDmpGWud9xGfz9hEF1hSTfG',
                        0.006, 'Litecoin', '3vB9hXHTCYbPiQNuyxCQgXF6AvFg51ozGKL9QkwoCwaS', 'litecoingw',
                        'wB-bg-LTC.png'), Gateway('----------', '3JeW3F1kEWxLsf8zg1uAZRPb7g5z6fuqEfF',
                                                  0.001, 'Bitcoin', '5Asy9P3xjcvBAgbeyiitZhBRJZJ2TPGSZJz9ihDTnB3d',
                                                  'bitcoingw', 'wB-bg-BTC.png'),
                Gateway('----------', '3JbigZzoGyFWksZ5RLuh9K5ntyGZuXKTVas',
                        0.001, 'Dash', 'A62sRG58HFbWUNvFoEEjX4U3txXKcLm11MXWWS429qpN', 'dashgw', 'wB-bg-DASH.png'),
                Gateway('----------', '3JsshGBTUXXqShXGQeNdtzw1EuQZFqxN4E3',
                        0.03, 'Wagerr', '91NnG9iyUs3ZT3tqK1oQ3ddpgAkE7v5Kbcgp2hhnDhqd', 'wagerrgw', 'wB-bg-WGR.png'),
                Gateway('----------', '3JiEjoFbgVKLVxdJYFD1HL9HYDN3RupVNHd',
                        0.003, 'Syscoin', 'HBxBjymrCC8TuL8rwCLr2vakDEq4obqkMwYYPEZtTauA', 'syscoingw', 'wB-bg-SYS.png'),
                Gateway('----------', '3JsenfjhSNRQsRZMXrkAtJMfjyzxrzSeCKr',
                        0.0003, 'BCH', 'Fr2kNhe7XR3E16W7Mfh7NhNcsQWLXx3hSLjoFgpbFsNj', 'bchgw', 'wB-bg-BCH.png'),
                Gateway('----------', '3Jve26ckLkBivDbryLzpvoLyoRfxUaAE7tE',
                        9, 'Dogecoin', 'HDeemVktm2Z68RMkyA7AexhpaCqot1By7adBzaN9j5Xg', 'dogegw', 'wB-bg-DOG.png'),
                Gateway('----------', '3Jbrk85BjtVtEyrVLVVF7yWjKcnGPA6Rk5C',
                        0.00041, 'Ethereum', '6Mh41byVWPg8JVCfuwG5CAPCh9Q7gnuaAVxjDfVNDmcD', 'ethgw', 'wB-bg-ETH.png')]
    return gateways
