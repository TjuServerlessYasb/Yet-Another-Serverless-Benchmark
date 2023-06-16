from ray import serve
import time
import json

from fi.model.post import PostItem
from fastapi import Body
from fi.service.message import GetMarginjson, GetPortfolios
from typing import List, Dict


def agg_timestamp(response, events, startTime, endTime, externalServicesTime):
    stampBegin = 1000 * time.time()
    prior = 0
    priorCost = 0
    priorServiceTime = 0
    workflowStartTime = startTime
    priorEndTime = 0
    externalServiceTimes = []

    for event in events:
        if 'workflowEndTime' in event and event['workflowEndTime'] > priorEndTime:
            priorEndTime = event['workflowEndTime']
            priorCost = event['timeStampCost']
        if 'workflowStartTime' in event and event['workflowStartTime'] < workflowStartTime:
            workflowStartTime = event['workflowStartTime']
        if 'externalServicesTime' in event and event['externalServicesTime'] > 0:
            externalServiceTimes.append(event['externalServicesTime'])

    priorServiceTime = max(externalServiceTimes) if len(externalServiceTimes) else 0

    # NOTE: This works only if the parallel step is the first step in the workflow
    prior = priorEndTime - workflowStartTime
    response['duration'] = prior + endTime - startTime
    response['workflowEndTime'] = endTime
    response['workflowStartTime'] = workflowStartTime
    response['externalServicesTime'] = priorServiceTime + externalServicesTime
    response['memsetTime'] = 0

    # Obscure code, doing to time.time() at the end of fn
    response['timeStampCost'] = priorCost - (stampBegin - 1000 * time.time())
    return response


def checkMarginBalance(portfolioData, marketData, portfolio):

    marginAccountBalance = GetMarginjson()[portfolio]
    print("get success")
    print(marginAccountBalance)
    print(">>>>>>>>")
    print(portfolioData)
    portfolioMarketValue = 0
    for trade in portfolioData:
        security = trade['Security']
        qty = trade['LastQty']
        portfolioMarketValue += qty * marketData[security]

    # Maintenance Margin should be atleast 25% of market value for "long" securities
    # https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210#the-rule
    result = False
    if marginAccountBalance >= 0.25 * portfolioMarketValue:
        result = True

    return result


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class MarginBalanceService(object):
    # def __init__(self):
    def MarginBalance(self, dic: List):

        try:
            #
            # events = json.loads(body)
            #
            # events = [json.loads(event) for event in events]
            print(dic)
            startTime = 1000 * time.time()
            marketData = {}
            validFormat = True

            for event in dic:
                body = event['body']
                if 'marketData' in body:
                    marketData = body['marketData']
                elif 'valid' in body:
                    portfolio = event['body']['portfolio']
                    validFormat = validFormat and body['valid']

            portfolios = GetPortfolios()
            portfolioData = portfolios[portfolio]
            print("show:::")
            print(portfolioData)
            print(marketData)
            print(portfolio)
            marginSatisfied = checkMarginBalance(portfolioData, marketData, portfolio)

            response = {'statusCode': 200,
                        'body': {'validFormat': validFormat, 'marginSatisfied': marginSatisfied}}

            endTime = 1000 * time.time()
            result = agg_timestamp(response, dic, startTime, endTime, 0)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return result
