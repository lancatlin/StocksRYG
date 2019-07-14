import requests
from bs4 import BeautifulSoup
import sys
from fake_useragent import UserAgent

def getPrice(stockNumber):
    # 取得最新的股價
    ua = UserAgent()
    url = 'http://tw.stock.yahoo.com/q/ts?s='+stockNumber
    header = {'User-Agent': ua.random}
    res = requests.get(url, header)
    soup = BeautifulSoup(res.text, 'html.parser')
    tr = soup.find('tr', bgcolor='#ffffff')
    td = tr.find_all('td')[3]
    return float(td.contents[0])

def req(stockNumber):
    ua = UserAgent()
    url = 'http://tw.stock.yahoo.com/d/s/dividend_'+stockNumber+'.html'
    header = {'User-Agent': ua.random}
    res = requests.get(url, header)
    return res.text

def parse(html):
    soup = BeautifulSoup(html, features="lxml")
    years = soup.find_all("tr", bgcolor="#FFFFFF")
    result = []
    for year in years:
        data = year.find_all("td")
        y = int(data[0].contents[0])
        money = float(data[1].contents[0])
        stock = float(data[4].contents[0])
        result.append({"year": y, "money": money, "stock": stock})
    return result

def Stock(stockNumber, years):
    price = getPrice(stockNumber)
    dividend = parse(req(stockNumber))
    allMoney = 0
    allDividend = 0
    for d in dividend[0:years]:
        allMoney += d["money"]
        allDividend += d['stock']
    totalReturn = ((allMoney / years) + (allDividend / years) * price  / 10) / price * 100
    print(price, allMoney, allDividend, totalReturn)
    return price, totalReturn
    
if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 3:
        price, totalReturn = Stock(argv[1], int(argv[2]))
        print(totalReturn, '%')
