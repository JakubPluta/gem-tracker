from ethplorer.client import EthplorerClient
import json
import pandas as pd
from datetime import datetime

with open('apikey.json') as f:
    api_key = json.load(f).get('api_key')
from datetime import datetime


# creator_address = "0x7c22958b42d0c5a45c32f3f097d1cf8ccce1d261"
# #creator_address2 = "0x42358f60f71b3ceedb7f6d4b72c0b3fee2853761"
# #token_address = "0xad0820827df41aa5e27b8b994db04837c0571540"


token_address = "0x9CDA02B2a43F16f11C6860A8630672de9854D6F7"
client = EthplorerClient(api_key)



class CheckTokenCreator:
    def __init__(self, client, token_address: str):
        self.client = client
        self.token_address = token_address
        self.token_info = client.get_address_info(token_address)
        self.creator_address = self.check_if_creator_data_exists(self.token_info)

    @staticmethod
    def check_if_creator_data_exists(token_info):
        contract_info = token_info.get('contractInfo')
        if contract_info and 'creatorAddress' in contract_info:
            return contract_info.get('creatorAddress')
        else:
            return None


# check = CheckTokenCreator(client=client, token_address=token_address)
#
# cr = check.creator_address


class TokenCreator:
    def __init__(self, creator_address, client):
        self.creator_address = creator_address
        self._creator_address_info = client.get_address_info(creator_address)
        self._creator_address_history = client.get_address_history(creator_address)

    def get_eth_balance(self):
        eth = self._creator_address_info.get("ETH")
        if eth:
            eth_balance = eth.get("balance")
            eth_current_price = eth.get("price").get("rate")
            usd_balance_value = round(int(eth_balance) * int(eth_current_price), 4)
            return {"ethBalance" : eth.get("balance"),"ethPrice" : eth.get("price").get("rate"), "usdBalance" : usd_balance_value}
        else:
            return None

    def get_transactions_count(self):
        return self._creator_address_info.get('countTxs')

    def get_info_about_creator_portfolio(self, json=False):
        portfolio_items = []
        portfolio = self._creator_address_info.get('tokens')
        if portfolio:
            for token in portfolio:
                token_dct = {}
                token_info = token.get('tokenInfo')
                balance = token.get('balance')
                token_dct['tokenAddress'] = token_info.get('address')
                token_dct['symbol'] = token_info.get('symbol')
                token_dct['name'] = token_info.get('name')
                token_dct['totalSupply'] = token_info.get('totalSupply')
                token_dct['balance'] = round(balance,2)
                try:
                    pct_of_supply = int(balance) / int(token_info.get('totalSupply'))
                except ZeroDivisionError:
                    pct_of_supply = None
                token_dct['pctOfTotalSupply'] = round(pct_of_supply, 4)
                portfolio_items.append(token_dct)
            if json:
                return portfolio_items
            else:
                return pd.DataFrame(portfolio_items)

    def get_transactions_info(self, json=False):
        transactions = []
        operations = self._creator_address_history.get('operations')
        if operations:
            for operation in operations:
                operation_dct = {}
                token_info = operation.get('tokenInfo')

                operation_dct['timestamp'] = operation.get('timestamp')

                try:
                    operation_dct['datetime'] = datetime.fromtimestamp(operation.get('timestamp'))
                except TypeError:
                    pass

                operation_dct['valueTransferred'] = operation.get('value')
                operation_dct['transferredFrom'] = operation.get('from')
                operation_dct['transferredTo'] = operation.get('to')
                if self.creator_address == operation.get('to'):
                    operation_dct['transferredToCreator'] = True
                else:
                    operation_dct['transferredToCreator'] = False
                if self.creator_address == operation.get('from'):
                    operation_dct['transferredFromCreator'] = True
                else:
                    operation_dct['transferredFromCreator'] = False

                operation_dct['tokenSymbol'] = token_info.get('symbol')
                operation_dct['tokenName'] = token_info.get('name')
                operation_dct['totalSupply'] = token_info.get('totalSupply')

                try:
                    transferred_pct = round(int(operation.get('value')) / int(token_info.get('totalSupply')),8)
                except ZeroDivisionError:
                    transferred_pct = None

                operation_dct['transferredPctOfTotalSupply'] = transferred_pct
                transactions.append(operation_dct)
            if json:
                return transactions
            else:
                return pd.DataFrame(transactions)



# creator = TokenCreator(cr, client)
#
# #print(creator.get_info_about_creator_portfolio(json=True))
#
# print(creator.get_transactions_info(True))


class TokenInfo:
    def __init__(self, token_address, client):
        self.client = client
        self.token_address = token_address
        self.token_info = self.client.get_token_info(token_address)


token_client = TokenInfo(token_address,client)

print(token_client.token_info)
