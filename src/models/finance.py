
from src.common.database import Database
from src.models.portfolio import Portfolio
from src.models.stock import Stock

class Finance(Stock):
    def __init__(self, portfolio_id, percent_change=None, total_purchase_value=None, total_current_value=None):
        self.portfolio_id = portfolio_id
        self.total_purchase_value = total_purchase_value
        self.total_current_value = total_current_value
        self.percent_change = percent_change

    def calculate_portfolio(self, portfolio_id):
        finance_data = Database.find_one('financedata', {"portfolio_id": self.portfolio_id})
        if finance_data is not None:
            Database.remove('financedata', {"portfolio_id": self.portfolio_id})
        stock_data = Database.find('stockdata', {"portfolio_id": portfolio_id})
        current_value_list = []
        add_price_list = []
        qty_list = []
        for data in stock_data:
            current_price = (data['current_price'])
            add_price = (data['add_price'])
            qty = (data['qty'])
            current_value_list.append(current_price)
            add_price_list.append(add_price)
            qty_list.append(qty)
        total_qty = sum(qty_list)
        total_current_value = sum(current_value_list)
        total_add_price = sum(add_price_list)
        print(total_current_value)
        try:
            total_purchase_value = total_add_price * total_qty
            total_current_value = total_current_value * total_qty
            percent_change = (total_current_value - total_purchase_value) / total_current_value

            finance = Finance(portfolio_id=portfolio_id, percent_change=percent_change,
                              total_purchase_value=total_purchase_value, total_current_value=total_current_value)
            finance.save_to_database()
        except ZeroDivisionError:
            print("You need to add data first!")

    @classmethod
    def find_finance_by_portfolio_id(cls, portfolio_id):
        stocks = Database.find(collection='financedata', query={"portfolio_id": portfolio_id})
        return [data for data in stocks]

    def save_to_database(self):
        Database.insert(collection='financedata', data=self.json())

    def json(self):
        return {
            "portfolio_id": self.portfolio_id,
            "total_purchase_value": self.total_purchase_value,
            "total_current_value": self.total_current_value,
            "percent_change": self.percent_change
        }

