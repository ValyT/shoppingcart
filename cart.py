import typing

from . import abc
import queue
import pandas as pd
import sqlite3

class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = dict()
        self._order = queue.Queue()
        self._price_list = dict(apple=1.0, banana=1.1, kiwi=3.0)

    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
            self._order.put(product_code)
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

    def print_receipt(self) -> typing.List[str]:
        lines = []
        total=0
        
        while not self._order.empty():
            
            product_code=self._order.get()
            amount=self._items[product_code]

            try:
                price = self._price_list[product_code] * amount
            except:
                price=0
            
            total+=price
            price_string = '€%.2f' % price

            lines.append(product_code + ' - ' + str(amount) + ' - ' + price_string)
        lines.append('Total = ' + '€%.2f' % total)
        return lines

    def import_prices(self, file_type: str, file_path: str):
        file_err = "File path or composition error"

        if file_type == 'csv':
            try:
                data = pd.read_csv(file_path)
            except:
                print(file_err)

        elif file_type == 'json':
            try:
                data = pd.read_json(file_path)
            except:
                print(file_err)

        elif file_type == 'sql':
            try:
                db = sqlite3.connect(file_path)
                query = 'SELECT product_code, price FROM products'
                data=pd.read_sql_query(query,db)
            except:
                print(file_err)

        else:
            print("Unsupported file type")

        data.columns=['product_code','price']
        for index,row in data.iterrows():
            product_code = row['product_code']
            price = row['price']
            self._price_list[product_code]=price

