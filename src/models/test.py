from src.models.stock import Stock
from src.common.database import Database
import json

Database.initialize('portfolio_database')

data = Database.find('stockdata', query={"portfolio_id": 'e59f06c6a3404195a8a2220134cddc74'})
li = []
li2 = []
for obj in data:
    # value = (data['total_price'])
    value = (obj['add_price'])
    value2 = (obj['qty'])
    li2.append(value2)
    li.append(value)

print(li)
print(li2)