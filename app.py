from flask import Flask, render_template, request
from stock import Stock
app = Flask(__name__)

@app.route('/')
def index():
    stock_number = request.args.get('stock_number')
    if stock_number == None: 
        return render_template('index.html', stock=None)
    try:
        stock = Stock(stock_number)
    except:
        return render_template('not_found.html', name=stock_number)
    return render_template('index.html', stock=stock)
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug = True)