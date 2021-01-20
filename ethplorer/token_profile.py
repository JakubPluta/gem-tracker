from ethplorer.client import EthplorerClient
import json
import pandas as pd
from datetime import datetime


class TokenInfo:
    def __init__(self, token_address, client):
        self.client = client
        self.token_address = token_address
        self.token_info = self.client.get_token_info(token_address)
        self.token_history = self.client.get_token_history(token_address)

    def get_token_history_of_transactions(self, dct_parse=False):
        transactions = []
        token_history = self.token_history.get('operations')
        if token_history:
            for operation in token_history:
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
                operation_dct['tokenSymbol'] = token_info.get('symbol')
                operation_dct['tokenName'] = token_info.get('name')
                operation_dct['totalSupply'] = token_info.get('totalSupply')
                try:
                    transferred_pct = round(float(operation.get('value')) / float(token_info.get('totalSupply')), 8)
                except ZeroDivisionError:
                    transferred_pct = None

                operation_dct['transferredPctOfTotalSupply'] = transferred_pct
                transactions.append(operation_dct)
            if dct_parse:
                return transactions
            else:
                return pd.DataFrame(transactions)

    def get_token_holders(self, dct_parse=False):
        token_holders = self.client.get_top_token_holders(self.token_address)
        if token_holders:
            holders = token_holders.get('holders')
            if dct_parse:
                return holders
            return pd.DataFrame(holders)

    def build_summary_of_token_transactions(self):
        token_history_cleaned = self.get_token_history_of_transactions(False)

        top_transferred_from = token_history_cleaned.groupby("transferredFrom").size()
        top_transferred_from.name = "countOfTransactionsTransferredFrom"
        top_transferred_from = top_transferred_from.sort_values(ascending=False).head(1)

        top_transferred_to = token_history_cleaned.groupby("transferredTo").size()
        top_transferred_to.name = "countOfTransactionsTransferredTo"
        top_transferred_to = top_transferred_from.sort_values(ascending=False).head(1)

        return {
            "totalTransactions" : len(token_history_cleaned),
            "firstTransactionDate" : token_history_cleaned['datetime'].min(),
            "lastTransactionDate" : token_history_cleaned['datetime'].max(),
            "addressWithHighestNumberOfTransfersTo" : top_transferred_to.index[0],
            "countTransfersTo" : top_transferred_to.values[0],
            "addressWithHighestNumberOfTransfersFrom": top_transferred_from.index[0],
            "countTransfersFrom": top_transferred_from.values[0]
        }


