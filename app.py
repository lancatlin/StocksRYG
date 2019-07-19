from flask import Flask, render_template, request
from stock import Stock
app = Flask(__name__)

@app.route('/')
def index():
    stock_number = request.args.get('stock_number')
    years = request.args.get('years')
    if stock_number == None or years == None: 
        return render_template('index.html', stock=None)
    try:
        years = int(years) 
    except:
        years = 1
    stock = Stock(stock_number, years)
    return render_template('index.html', stock=stock)
        
if __name__ == "__main__":
    app.run(debug = True)