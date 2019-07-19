# StocksRYG 股票紅綠燈

使用歷年股利，計算出股利的投資報酬率，分辨出**長期穩健的股票**。

## 計算公式
```
總投資報酬率 = (現金股利 + 股票股利 * 股價 / 10) / 股價
```

### 資料來源
[Yahoo 股市](https://tw.stock.yahoo.com)  
本程式使用爬蟲取得資料，可能因 Yahoo 網站改版或政策改變而無法使用。

## 安裝
Python 版本 3.7
```
git clone https://github.com/lancatlin/StocksRYG
cd StocksRYG
pip3 install -r requirements.txt
```

## 運行
網頁界面：
```
python3 app.py
```
指令界面：
```
python3 stock.py 股票號碼 採計年數
```
