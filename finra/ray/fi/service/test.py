from benchmark.ray.finra.fi.service.message import GetPortfolios

if __name__ == '__main__':
    zz = [{"body": {"portfolioType": "S&P", "portfolio": "1234"}},{"body": {"portfolioType": "S&P", "portfolio": "1234"}},{"body": {"portfolioType": "S&P", "portfolio": "1234"}}]
    print(type(zz))
    for lab in zz:
        print(type(lab))

