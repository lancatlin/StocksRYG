import requests
from bs4 import BeautifulSoup
import sys
from fake_useragent import UserAgent

class Stock:
    def __init__(self, stockNumber, years):
        price = self.getPrice(stockNumber)
        html = self.req(stockNumber)
        dividend = self.parse(html)
        allMoney = 0
        allDividend = 0
        for d in dividend[0:years]:
            allMoney += d["money"]
            allDividend += d['stock']
        totalReturn = ((allMoney / years) + (allDividend / years) * price  / 10) / price * 100
        self.number = stockNumber
        self.years = years
        self.price = price
        self.money = round(allMoney / years, 2)
        self.dividend = round(allDividend / years, 2)
        self.total = round(totalReturn, 2)

    def req(self, stockNumber):
        ua = UserAgent()
        url = 'http://tw.stock.yahoo.com/d/s/dividend_'+stockNumber+'.html'
        header = {'User-Agent': ua.random}
        res = requests.get(url, header)
        return res.text

    def parse(self, html):
        soup = BeautifulSoup(html, features="lxml")
        self.name = soup.find("font", color="#F70000").contents[0].contents[0]
        years = soup.find_all("tr", bgcolor="#FFFFFF")
        result = []
        for year in years:
            data = year.find_all("td")
            y = int(data[0].contents[0])
            money = float(data[1].contents[0])
            stock = float(data[4].contents[0])
            result.append({"year": y, "money": money, "stock": stock})
        return result

    def getPrice(self, stockNumber):
        # 取得最新的股價
        ua = UserAgent()
        url = 'http://tw.stock.yahoo.com/q/ts?s='+stockNumber
        header = {'User-Agent': ua.random}
        res = requests.get(url, header)
        soup = BeautifulSoup(res.text, 'html.parser')
        tr = soup.find('tr', bgcolor='#ffffff')
        td = tr.find_all('td')[3]
        return float(td.contents[0])
    
if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 3:
        stock = Stock(argv[1], int(argv[2]))
        print('{}: {:.2f}%'.format(stock.name, stock.total))
