from pycoingecko import CoinGeckoAPI
import re
import nltk


cg = CoinGeckoAPI()

token_address = "0x9cda02b2a43f16f11c6860a8630672de9854d6f7"

list_of_tokens = cg.get_coins_list()

token_name = "TOM"

def find_similar_coins_on_coingecko(token_name):
    list_of_tokens = cg.get_coins_list()
    simmilar = [token for token in list_of_tokens if re.match(fr"^{token_name}.?", token["symbol"], flags=re.IGNORECASE)]
    return simmilar



lisst = find_similar_coins_on_coingecko(token_name)

def get_similar_tokens_data(list_of_similar_tokens):
    coins = []
    for l in list_of_similar_tokens:
        coin = cg.get_coin_by_id(l.get('id'))
        coin_dct = {
            'id': coin.get('id'),
            'symbol': coin.get('symbol'),
            'name': coin.get('name'),
            'platform': coin.get('asset_platform_id'),
            'description': coin.get('description').get('en'),
            'links': coin.get('links'),
            'country_origin': coin.get('country_origin'),
            "contract_address": coin.get("contract_address"),
        }
        coins.append(coin_dct)

    return coins

x = get_similar_tokens_data(lisst)

