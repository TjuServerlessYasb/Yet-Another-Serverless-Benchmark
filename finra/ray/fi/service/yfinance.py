from ray import serve

from typing import List, Dict

data = {
  'GOOG': '{"chart":{"result":[{"meta":{"currency":"USD","symbol":"GOOG","exchangeName":"NMS","instrumentType":"EQUITY","firstTradeDate":1092922200,"regularMarketTime":1656360004,"gmtoffset":-14400,"timezone":"EDT","exchangeTimezoneName":"America/New_York","regularMarketPrice":2332.45,"chartPreviousClose":2370.76,"priceHint":2,"currentTradingPeriod":{"pre":{"timezone":"EDT","end":1656423000,"start":1656403200,"gmtoffset":-14400},"regular":{"timezone":"EDT","end":1656446400,"start":1656423000,"gmtoffset":-14400},"post":{"timezone":"EDT","end":1656460800,"start":1656446400,"gmtoffset":-14400}},"dataGranularity":"1d","range":"1","validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]},"timestamp":[1656336600],"indicators":{"quote":[{"volume":[1641500],"close":[2332.449951171875],"high":[2385.0],"open":[2378.699951171875],"low":[2320.014892578125]}],"adjclose":[{"adjclose":[2332.449951171875]}]}}],"error":null}}',
  'AMZN': '{"chart":{"result":[{"meta":{"currency":"USD","symbol":"AMZN","exchangeName":"NMS","instrumentType":"EQUITY","firstTradeDate":863703000,"regularMarketTime":1656360004,"gmtoffset":-14400,"timezone":"EDT","exchangeTimezoneName":"America/New_York","regularMarketPrice":113.22,"chartPreviousClose":116.46,"priceHint":2,"currentTradingPeriod":{"pre":{"timezone":"EDT","end":1656423000,"start":1656403200,"gmtoffset":-14400},"regular":{"timezone":"EDT","end":1656446400,"start":1656423000,"gmtoffset":-14400},"post":{"timezone":"EDT","end":1656460800,"start":1656446400,"gmtoffset":-14400}},"dataGranularity":"1d","range":"1","validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]},"timestamp":[1656336600],"indicators":{"quote":[{"open":[117.08999633789062],"high":[117.9800033569336],"volume":[62071500],"low":[112.69999694824219],"close":[113.22000122070312]}],"adjclose":[{"adjclose":[113.22000122070312]}]}}],"error":null}}',
  'MSFT': '{"chart":{"result":[{"meta":{"currency":"USD","symbol":"MSFT","exchangeName":"NMS","instrumentType":"EQUITY","firstTradeDate":511108200,"regularMarketTime":1656360004,"gmtoffset":-14400,"timezone":"EDT","exchangeTimezoneName":"America/New_York","regularMarketPrice":264.89,"chartPreviousClose":267.7,"priceHint":2,"currentTradingPeriod":{"pre":{"timezone":"EDT","start":1656403200,"end":1656423000,"gmtoffset":-14400},"regular":{"timezone":"EDT","start":1656423000,"end":1656446400,"gmtoffset":-14400},"post":{"timezone":"EDT","start":1656446400,"end":1656460800,"gmtoffset":-14400}},"dataGranularity":"1d","range":"1","validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]},"timestamp":[1656336600],"indicators":{"quote":[{"volume":[24600800],"open":[268.2099914550781],"close":[264.8900146484375],"low":[263.2799987792969],"high":[268.29998779296875]}],"adjclose":[{"adjclose":[264.8900146484375]}]}}],"error":null}}'}



@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class YfinanceService(object):
    # def __init__(self):
    def Yfinance(self, body: Dict) -> Dict:
        r = body['body']
        print(data[r])
        print(type(data[r]))

        return data[r]