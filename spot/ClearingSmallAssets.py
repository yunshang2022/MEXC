import mexc_spot_v3

#获取价格函数
def get_avgprice(symbol):
    market = mexc_spot_v3.mexc_market()
    params = {
        "symbol":symbol ,#"BTCUSDT"
    }
    AvgPrice = market.get_avgprice(params)
    # print(AvgPrice)
    # print(AvgPrice['price'])
    Price=float(AvgPrice['price'])
    return AvgPrice['price']

#平仓函数
def post_order(symbol,quantity):
    trade = mexc_spot_v3.mexc_trade()
    params = {
        "symbol": symbol,
        "side": "SELL",
        "type": "MARKET",
        "quantity": quantity
    }
    PlaceOrder = trade.post_order(params)
    print(PlaceOrder)
    return PlaceOrder

#小额兑换
def smallAssets_convert(asset):
    wallet = mexc_spot_v3.mexc_wallet()
    params = {
        "asset": asset
    }
    Convert = wallet.post_smallAssets_convert(params)
    print(Convert)
    return Convert

#主函数
def main():
    try:
        trade = mexc_spot_v3.mexc_trade()
        AccountInfo = trade.get_account_info()
        # print(AccountInfo)
        # print(AccountInfo['balances'])
        for balance in AccountInfo['balances']:
            if "USDT" not in balance['asset']: #USDT的资产不卖
                symbol=balance['asset']+"USDT"
                print(symbol)
                avgprice=get_avgprice(symbol)
                free=float(balance['free'])
                if free * avgprice < 50 and free * avgprice > 5:  #小于50U的资产全部平仓
                    #全部卖出
                    OrderID = post_order(symbol,balance['free'])
                    if OrderID:
                        print(f"{symbol}卖出{free},成功")
                    else:
                        print(f"{symbol}卖出{free},不成功!!!")
                elif free * avgprice <=5:
                    convertID = smallAssets_convert(balance['asset'])
                    if convertID:
                        print(f"{balance['asset']}小额兑换{free},成功")
                    else:
                        print(f"{balance['asset']}小额兑换{free},不成功!!!")

    except e:
        print("代码错误!",e)

if __name__ == "__main__":
    main()