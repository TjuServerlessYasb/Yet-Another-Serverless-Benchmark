import time
import json
import datetime

from ray import serve
from fi.model.post import PostItem
from fastapi import Body
from fi.service.message import GetPortfolios


def timestamp(response, event, startTime, endTime, externalServicesTime):
    stampBegin = 1000 * time.time()
    prior = event['duration'] if 'duration' in event else 0
    priorMemSet = event['memsetTime'] if 'memsetTime' in event else 0
    priorServiceTime = event['externalServicesTime'] if 'externalServicesTime' in event else 0
    response['duration'] = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = event['workflowStartTime'] if 'workflowStartTime' in event else startTime
    priorCost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['externalServicesTime'] = priorServiceTime + externalServicesTime
    response['memsetTime'] = priorMemSet
    response['timeStampCost'] = priorCost - (stampBegin - 1000 * time.time())
    return response


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class TrddateService(object):

    def Trddate(self, body: PostItem = Body(embed=True)):
        startTime = 1000 * time.time()



        portfolio = body.portfolio

        portfolios = GetPortfolios()
        print(type(portfolios))
        data = portfolios[portfolio]
        print(data)

        valid = True

        for trade in data:
            trddate = trade['TradeDate']
            # Tag ID: 75, Tag Name: TradeDate, Format: YYMMDD
            if len(trddate) == 6:
                try:
                    datetime.datetime(int(trddate[0:2]), int(trddate[2:4]), int(trddate[4:6]))
                except ValueError:
                    valid = False
                    break
            else:
                valid = False
                break

        response = {'statusCode': 200, 'body': {'valid': valid, 'portfolio': portfolio}}
        endTime = 1000 * time.time()
        return timestamp(response, body, startTime, endTime, 0)
