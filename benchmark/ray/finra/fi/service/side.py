import time
from ray import serve

from fi.model.post import PostItem
from fastapi import Body
from fi.service.message import GetPortfolios
from typing import List, Dict

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
class SideService(object):
    def Side(self, body: Dict):
        try:

            startTime = 1000 * time.time()
            portfolio = body['body']['portfolio']
            portfolios = GetPortfolios()
            data = portfolios[portfolio]

            valid = True

            for trade in data:
                side = trade['Side']
                # Tag ID: 552, Tag Name: Side, Valid values: 1,2,8
                if not (side == 1 or side == 2 or side == 8):
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