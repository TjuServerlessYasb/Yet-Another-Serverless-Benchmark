from ray import serve
from typing import List, Dict
import time

from fi.service.message import GetPortfolios


def timestamp(response, event, startTime, endTime, externalServicesTime):
    stampBegin = 1000*time.time()
    prior = event['duration'] if 'duration' in event else 0
    priorMemSet = event['memsetTime'] if 'memsetTime' in event else 0
    priorServiceTime = event['externalServicesTime'] if 'externalServicesTime' in event else 0
    response['duration']     = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['externalServicesTime'] = priorServiceTime + externalServicesTime
    response['memsetTime'] = priorMemSet
    response['timeStampCost'] = priorCost - (stampBegin-1000*time.time())
    return response

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class LastpxService(object):
    # def __init__(self):
    def Lastpx(self, body: Dict):
        """handle a request to the function
        Args:
            req (str): request body
        """
        # event = json.loads(body)
        print(123)


        try:
            print(body)
            startTime = 1000 * time.time()
            # portfolio = body.values().body.portfolio
            portfolio = body['body']['portfolio']
            portfolios = GetPortfolios()
            data = portfolios[portfolio]


            valid = True

            for trade in data:
                px = str(trade['LastPx'])
                if '.' in px:
                    a, b = px.split('.')
                    if not ((len(a) == 3 and len(b) == 6) or
                            (len(a) == 4 and len(b) == 5) or
                            (len(a) == 5 and len(b) == 4) or
                            (len(a) == 6 and len(b) == 3)):
                        print('{}: {}v{}'.format(px, len(a), len(b)))
                        valid = False
                        break

            response = {'statusCode': 200, 'body': {'valid': valid, 'portfolio': portfolio}}

            endTime = 1000 * time.time()
            result = timestamp(response, body, startTime, endTime, 0)
            print(result)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return result

