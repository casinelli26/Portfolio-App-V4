from src.models.stock import Stock
from src.common.database import Database
import json

Database.initialize('portfolio_database')

data = Database.find('stockdata', query={"portfolio_id": '602cee09f7cf42b5b3d452d2e1c119d4'})
li = []
for obj in data:
    # value = (data['total_price'])
    print(obj)
    value = (obj['total_price'])
    print(value)
    li.append(value)

print(li)