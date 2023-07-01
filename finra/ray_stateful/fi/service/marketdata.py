from ray import serve
from typing import List, Dict
import time
import ray
from fi.service.market.base import Ticker
financedata = {}
a = 0
@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class MarketdataService(object):
    # def __init__(self):
    def Marketdata(self, body: Dict):
        """handle a request to the function
        Args:
            req (str): request body
        """
        # event = json.loads(body)
        print(123)


        try:
            startTime = time.time()
            externalServicesTime = []
            portfolioType = body['body']['portfolioType']

            tickersForPortfolioTypes = {'S&P': ['GOOG', 'AMZN', 'MSFT']}
            tickers = tickersForPortfolioTypes[portfolioType]
            print("tickers:")
            print(tickers)
            print(len(tickers))
            prices = {}
            for ticker in tickers:
                tickTime = time.time()
                global financedata
                if ticker in financedata:
                    print(type(financedata[ticker]))
                    data = ray.get(financedata[ticker])
                    print("存在")
                else:
                    print("不存在")
                    tickerObj = Ticker(ticker)
                    print(tickerObj)
                    # Get last closing price

                    data = tickerObj.history(period="1")
                    print("data:")
                    print(data)
                    financedata[ticker] = ray.put(data)

                global a
                a += 1
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", a)

                # tickerObj = Ticker(ticker)
                # print(tickerObj)
                # # Get last closing price
                # tickTime = time.time()
                # data = tickerObj.history(period="1")
                # print("data:")
                # print(data)
                externalServicesTime.append(time.time() - tickTime)
                price = data['Close'].unique()[0]
                prices[ticker] = price

            # prices = {'GOOG': 1732.38, 'AMZN': 3185.27, 'MSFT': 221.02}

            endTime = time.time()

            response = {'time': {'start': startTime, 'end': endTime, 'externalServicesTime': externalServicesTime},
                        'body': {'marketData': prices}}
            print(response)
            # return response


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return ray.put(response)