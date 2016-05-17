from src.common.database import Database
from src.common.errors import StockDoesNotExist, StockAlreadyExist
import uuid
import datetime
import locale


class Stock(object):
    def __init__(self, ticker=None, portfolio_id=None, qty=None, add_price=None,
                 add_date=datetime.datetime.now(), stock_id=None,
                 current_price=None, total_price=None):
        self.ticker = ticker if ticker is None else ticker.upper()
        self.qty = qty
        self.add_price = add_price
        self.current_price = add_price if current_price is None else current_price
        self.stock_id = uuid.uuid4().hex if stock_id is None else stock_id
        self.add_date = add_date
        self.portfolio_id = portfolio_id
        self.total_price = total_price
        self.current_date = datetime.datetime.now()
        self.days_in_portfolio = str((self.current_date - self.add_date))

    def new_stock(self, ticker, qty):
        from yahoo_finance import Share
        stock_data = Database.find_one(collection='stockdata', query={"ticker": self.ticker})
        if stock_data is not None:
            raise StockAlreadyExist("This stock has already been entered into portfolio.")
        else:
            locale.setlocale(locale.LC_ALL, '')
            company = Share(ticker)
            add_price = company.get_price()
            add_price = float(add_price)
            stock = Stock(portfolio_id=self.portfolio_id,
                          ticker=ticker,
                          qty=qty,
                          add_price=add_price,
                          total_price=float(add_price) * float(qty))
            stock.save_to_database()

    def update_stock_data(self, ticker, qty):
        stock_data = Database.find_one('stockdata', {"ticker": self.ticker})
        add_price = stock_data['add_price']
        if stock_data is None:
            raise StockDoesNotExist("Stock does not exist in Database")
        else:
            Database.remove('stockdata', query={"ticker": self.ticker})
            from yahoo_finance import Share
            locale.setlocale(locale.LC_ALL, '')
            company = Share(ticker)
            update_price = company.get_price()
            update_price = float(update_price)
            stock = Stock(portfolio_id=self.portfolio_id,
                          ticker=ticker,
                          qty=qty,
                          current_price=update_price,
                          add_price=add_price,
                          total_price=float(update_price) * float(qty))
            stock.save_to_database()

    @classmethod
    def find_stock_by_portfolio_id(cls, portfolio_id):
        stocks = Database.find(collection='stockdata', query={"portfolio_id": portfolio_id})
        return [data for data in stocks]

    def save_to_database(self):
        Database.insert(collection='stockdata', data=self.json())

    def delete_stock_data(self):
        stock_data = Database.find_one(collection='stockdata', query={"ticker": self.ticker})
        if stock_data is None:
            raise StockDoesNotExist("Stock does not exist in database")
        else:
            Database.remove(collection='stockdata', query={"ticker": self.ticker})

    def json(self):
        return {
            "ticker": self.ticker,
            "qty": self.qty,
            "add_price": self.add_price,
            "current_price": self.current_price,
            "stock_id": self.stock_id,
            "add_date": self.add_date,
            "portfolio_id": self.portfolio_id,
            "total_price": self.total_price,
            "days_in_portfolio": self.days_in_portfolio
        }