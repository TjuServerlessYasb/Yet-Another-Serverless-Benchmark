import requests
import json

headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    }


#req = '{"body":{ "portfolioType":"S&P", "portfolio":"1234"}}'


# req = { "portfolioType":"S&P", "portfolio":"1234"}

req = {"body":{ "portfolioType":"S&P", "portfolio":"1234"}}
resp3 = requests.post("http://10.244.0.158:8000/fi/marketdata", data=json.dumps(req), headers=headers)

req = {"body":{ "portfolioType":"S&P", "portfolio":"1234"}}
resp3 = requests.post("http://10.244.0.158:8000/fi/lastpx", data=json.dumps(req), headers=headers)

print(resp3.text)

resp3 = requests.post("http://10.244.0.158:8000/fi/side", data=json.dumps(req), headers=headers)

print(resp3.text)

resp3 = requests.post("http://10.244.0.158:8000/fi/trddate", data=json.dumps(req), headers=headers)

print(resp3.text)
resp3 = requests.post("http://10.244.0.158:8000/fi/volume", data=json.dumps(req), headers=headers)

print(resp3.text)

# req = {"body":"MSFT"}
#
# resp3 = requests.post("http://10.244.0.158:8000/fi/yfinance", data=json.dumps(req), headers=headers)

print(resp3.text)

