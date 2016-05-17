from src.common.database import Database
import datetime
import uuid

class Portfolio(object):
    def __init__(self, portfolio_name=None, portfolio_description=None,
                 date_created=datetime.datetime.now(), portfolio_id=None, total_value=None):
        self.portfolio_name = portfolio_name
        self.date_created = date_created
        self.portfolio_description = portfolio_description
        self.portfolio_id = uuid.uuid4().hex if portfolio_id is None else portfolio_id
        self.total_value = total_value

    @staticmethod
    def find_by_portfolio_id(portfolio_id):
        portfolios = Database.find(collection='portfolio_data', query={"portfolio_id": portfolio_id})
        return [portfolio for portfolio in portfolios]

    def save_to_database(self):
        Database.insert(collection='portfolio_data', data=self.json())

    @staticmethod
    def calculate_total(portfolio_id):
        data = Database.find('stockdata', {"portfolio_id": portfolio_id})
        li = []
        for total in data:
            value = (data['total_price'])
            li.append(value)
        total_value = sum(li)
        return total_value


    @staticmethod
    def get_portfolio():
        portfolio_data = Database.showcollection('portfolio_data')
        return [data for data in portfolio_data]

    def json(self):
        return {
            "portfolio_name": self.portfolio_name,
            "date_created": self.date_created,
            "portfolio_description": self.portfolio_description,
            "portfolio_id": self.portfolio_id,
            "total_value": self.total_value
        }