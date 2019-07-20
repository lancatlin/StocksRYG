import requests
from bs4 import BeautifulSoup
import sys
from fake_useragent import UserAgent
from enum import Enum

class StockGrade:
    RED = '#ff3c38' 
    YELLOW = '#fde74c'
    GREEN = '#81e979'

class Stock:
    def __init__(self, stockNumber):
        price = self.getPrice(stockNumber)
        html = self.req(stockNumber)
        self.years = self.parse(html)
        self.number = stockNumber
        self.price = price

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
            result.append(Year(y, money, stock))
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

    def light(self, years):
        roi = self.ROI(years)
        if roi > 8:
            return StockGrade.GREEN
        elif roi > 5:
            return StockGrade.YELLOW
        else:
            return StockGrade.RED
    
    def ROI(self, years):
        allMoney = 0
        allDividend = 0
        for d in self.years[0:years]:
            allMoney += d.money
            allDividend += d.dividend
        return round(((allMoney / years) + (allDividend / years) * self.price  / 10) / self.price * 100, 2)

class Year:
    def __init__(self, year, money, dividend):
        self.year = year
        self.money = money
        self.dividend = dividend

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 3:
        stock = Stock(argv[1], int(argv[2]))
        print('{}: {:.2f}%'.format(stock.name, stock.total))
