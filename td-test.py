import tdameritrade as td
import os
import json

client_id = os.getenv('td_client_id')
account_id = os.getenv('td_account_id')
refresh_token = os.getenv('td_refresh_token')

tdc = td.TDClient(client_id=client_id,refresh_token=refresh_token,account_ids=[account_id])

quantity = 1
symbol = 'PFE_021822C56'
buyprice = 0.92
sellprice = 1.38
stoplimit = 0.46

orderdata = {
    "orderStrategyType": "TRIGGER",
    "session": "NORMAL",
    "duration": "FILL_OR_KILL",
    "orderType": "LIMIT",
    "price": buyprice,
    "orderLegCollection": [
        {
            "instruction": "BUY_TO_OPEN",
            "quantity": quantity,
            "instrument": {
                "symbol": symbol,
                "assetType": "OPTION"
            }
        }
    ],
    "childOrderStrategies": [
        {
            "orderStrategyType": "OCO",
            "childOrderStrategies": [
                {
                    "orderStrategyType": "SINGLE",
                    "session": "NORMAL",
                    "duration": "GOOD_TILL_CANCEL",
                    "orderType": "LIMIT",
                    "price": sellprice,
                    "orderLegCollection": [
                        {
                            "instruction": "SELL_TO_CLOSE",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "OPTION"
                            }
                        }
                    ]
                },
                {
                    "orderStrategyType": "SINGLE",
                    "session": "NORMAL",
                    "duration": "GOOD_TILL_CANCEL",
                    "orderType": "STOP_LIMIT",
                    "stopPriceLinkBasis": "BID",
                    "stopPriceLinkType": "VALUE",
                    "stopPrice": stoplimit,
                    "price": stoplimit,
                    "orderLegCollection": [
                        {
                            "instruction": "SELL_TO_CLOSE",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "OPTION"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
orderjson = json.dumps(orderdata)

tdc.placeOrder(account_id, orderjson)
