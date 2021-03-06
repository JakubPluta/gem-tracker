from ethplorer.client import EthplorerClient
from ethplorer.creator_profile import TokenCreator, CheckTokenCreator
from ethplorer.token_profile import TokenInfo
from ethplorer.client import EthplorerClient
from tabulate import tabulate
import json
import pandas as pd


with open('ethplorer/apikey.json') as f:
    api_key = json.load(f).get('api_key')


def generate(token_address, api_key):
    if not api_key:
        raise ValueError("Api key missing")


    client = EthplorerClient(api_key)
    token = TokenInfo(token_address, client)

    # Tokens information

    token_summary = [token.build_summary_of_token_transactions()]
    token_holders = token.get_token_holders(True)
    token_info = [token.token_info]

    print()
    print(50 * ">", "Token Info", 50 * "<")
    print()
    print(tabulate(token_info, headers='keys'))
    print()

    print()
    print(50 * ">", "Token Holders", 50 * "<")
    print()
    print(tabulate(token_holders, headers='keys'))
    print()
    print()
    print(50 * ">", "Token Transactions Summary", 50 * "<")
    print()
    print(tabulate(token_summary, headers='keys'))
    print()

    # Check if creator exists ?
    creator_address = CheckTokenCreator(token_address, client).creator_address

    if creator_address is not None:
        creator = TokenCreator(creator_address, client)

        portfolio = creator.get_info_about_creator_portfolio(True)
        eth = creator.get_eth_balance()
        print()
        print()
        print(50 * ">", "Contract Creator Info Found", 50 * "<")
        print()
        print(f"################ Contract creator address: {creator_address}")
        print(f"################ Transactions count: {creator.get_transactions_count()}")
        print(f"################ ETH Balance: {eth.get('ethBalance')} ETH")
        print(f"################ USD Balance: {eth.get('usdBalance')} USD")
        print()
        print(tabulate(portfolio, headers="keys"))
        print()
        print()
        print(50 * ">", "Contract Creator Transactions", 50 * "<")
        print()
        transactions = creator.get_transactions_info(True)
        tab2 = tabulate(transactions, headers="keys")
        print(tab2)
    else:
        print(50 * ">", "Contract Creator Info Not Found", 50 * "<")

    # coingecko

    from coingecko.gecko import find_similar_coins_on_coingecko, get_similar_tokens_data
    token_symbols = token.token_info.get('symbol')
    list_of_sim_tokens = find_similar_coins_on_coingecko(token_symbols)

    similar = get_similar_tokens_data(list_of_sim_tokens, token_address)
    print()
    print()
    print(50 * ">", "Similar Coins Founded on CoinGecko", 50 * "<")
    print()
    tab3 = tabulate(similar, headers="keys")
    print(tab3)


#generate("0x9cda02b2a43f16f11c6860a8630672de9854d6f7")