from ethplorer.client import EthplorerClient
import json
import pandas as pd
from datetime import datetime
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.12f')


class CheckTokenCreator:
    def __init__(self, token_address: str, client):
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
            usd_balance_value = round(float(eth_balance) * float(eth_current_price), 8)
            return {"ethBalance" : eth.get("balance"),"ethPrice" : eth.get("price").get("rate"), "usdBalance" : usd_balance_value}
        else:
            return None

    def get_transactions_count(self):
        return self._creator_address_info.get('countTxs')

    def get_info_about_creator_portfolio(self, dct_parse=False):
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
                token_dct['balance'] = float(balance)
                try:
                    pct_of_supply = float(balance) / float(token_info.get('totalSupply'))
                except ZeroDivisionError:
                    pct_of_supply = None
                token_dct['pctOfTotalSupply'] = round(pct_of_supply, 8)
                portfolio_items.append(token_dct)
            if dct_parse:
                return portfolio_items
            else:
                return pd.DataFrame(portfolio_items)

    def get_transactions_info(self, dct_parse=False):
        transactions = []
        operations = self._creator_address_history.get('operations')
        if operations:
            for operation in operations:
                operation_dct = {}
                token_info = operation.get('tokenInfo')

                #operation_dct['timestamp'] = operation.get('timestamp')

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
                    transferred_pct = round(float(operation.get('value')) / float(token_info.get('totalSupply')),6)
                except ZeroDivisionError:
                    transferred_pct = None

                operation_dct['transferredPct'] = transferred_pct
                transactions.append(operation_dct)
            if dct_parse:
                return transactions
            else:
                return pd.DataFrame(transactions)
