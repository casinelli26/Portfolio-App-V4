from src.common.database import Database
from src.models.portfolio import Portfolio
from src.models.stock import Stock
import uuid
from flask import Flask, render_template, request, session, make_response, flash
from src.common.errors import StockError
from src.models.finance import Finance

app = Flask(__name__)  # '__main__'
app.secret_key = "my secret key"


@app.before_first_request
def initialize_database():
    Database.initialize('portfolio_database')


@app.route('/portfolio-home')
def portfolio_home():
    portfolios = Portfolio.get_portfolio()
    return render_template('portfolio.html', portfolios=portfolios)


@app.route('/portfolio/new', methods=['POST', 'GET'])
def create_new_portfolio():
    if request.method == 'GET':
        return render_template('new_portfolio.html')
    else:
        title = request.form['portfolio_name']
        description = request.form['portfolio_description']
        new_portfolio = Portfolio(portfolio_name=title, portfolio_description=description, portfolio_id=uuid.uuid4().hex)
        new_portfolio.save_to_database()
        return make_response(portfolio_home())


@app.route('/portfolio/<string:portfolio_id>', methods=['GET'])
def portfolio_holdings(portfolio_id):
    portfolios = Portfolio.find_by_portfolio_id(portfolio_id)
    stocks = Stock.find_stock_by_portfolio_id(portfolio_id)
    finance_data = Finance.find_finance_by_portfolio_id(portfolio_id)
    for data in finance_data:
        print(data)
    return render_template('portfolio_detail.html', portfolios=portfolios, stocks=stocks, finance_data=finance_data)


@app.route('/portfolio/<string:unique_ticker>')
def stock_detail(unique_ticker):
    stocks = Stock.find_stock_by_unique_ticker(unique_ticker=unique_ticker)
    return render_template('stock_detail.html', stocks=stocks)


@app.route('/portfolio/<string:portfolio_id>/add', methods=['POST', 'GET'])
def add_stock(portfolio_id):
    if request.method == 'GET':
        return render_template('add_stock.html', portfolio_id=portfolio_id)
    else:
        try:
            ticker = request.form['ticker']
            qty = request.form['qty']
            new_stock = Stock(portfolio_id=portfolio_id, ticker=ticker, qty=qty)
            new_stock.new_stock(qty=qty, ticker=ticker)
            finance = Finance(portfolio_id=portfolio_id)
            finance.calculate_portfolio(portfolio_id)
            flash("Stock added!")
            return make_response(portfolio_holdings(portfolio_id))
        except StockError as e:
            return e.message


@app.route('/portfolio/<string:portfolio_id>/update', methods=['POST', 'GET'])
def update_stocks(portfolio_id):
    if request.method == 'GET':
        return render_template('update_stock.html', portfolio_id=portfolio_id)
    else:
        try:
            ticker = request.form['ticker']
            qty = request.form['qty']
            update_stock = Stock(portfolio_id=portfolio_id, ticker=ticker, qty=qty)
            update_stock.update_stock_data(ticker=ticker, qty=qty)
            finance = Finance(portfolio_id=portfolio_id)
            finance.calculate_portfolio(portfolio_id)
            return make_response(portfolio_holdings(portfolio_id))
        except StockError as e:
            return e.message


@app.route('/portfolio/<string:portfolio_id>/delete', methods=['POST', 'GET'])
def delete_stocks(portfolio_id):
    if request.method == 'GET':
        return render_template('delete_stock.html', portfolio_id=portfolio_id)
    else:
        try:
            ticker = request.form['ticker']
            stock = Stock(portfolio_id=portfolio_id, ticker=ticker, qty=None)
            stock.delete_stock_data()
            finance = Finance(portfolio_id=portfolio_id)
            finance.calculate_portfolio(portfolio_id)
            return make_response(portfolio_holdings(portfolio_id=portfolio_id))
        except StockError as e:
            return e.message