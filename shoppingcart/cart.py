from tkinter import END
import typing

from . import abc
import queue
import pandas as pd
import sqlite3

class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        #Items and quantitites
        self._items = dict()
        #Queue used to preserve order of items in cart
        self._order = queue.Queue()
        #Persistent price list, can be updated, replaced the find price function
        #TODO Assumed we didn't want a second class
        #that being said the price list isn't something necessarily assoiciated with a cart
        #should probably be on a different price and stock management system
        self._price_list = dict(apple=1.0, banana=1.1, kiwi=3.0)
        #Currency that transactions are made in
        #TODO Assumed prices would stay the same regardless of currency
        #might want to implement some sort of currency conversion system
        #however that should also probably be part of the aforementioned price and stock management system
        self.currency = '€'

    #Adding items to ths shopping cart
    def add_item(self, product_code: str, quantity: int):
        if product_code not in self._items:
            self._items[product_code] = quantity
            self._order.put(product_code)
        else:
            q = self._items[product_code]
            self._items[product_code] = q + quantity

    #Finalysing purchase and printing receipt
    def print_receipt(self) -> typing.List[str]:
        lines = []
        total = 0
        
        while not self._order.empty():
            
            #Using the order queue to ensure items are printed in the order they are added
            product_code=self._order.get()
            amount=self._items[product_code]

            #If an item isn't in the price list, the price will be 0
            try:
                price = self._price_list[product_code] * amount
            except:
                price=0
            
            total+=price
            price_string = self.currency+'%.2f' % price

            lines.append(product_code + ' - ' + str(amount) + ' - ' + price_string)
        #Purchase total
        lines.append('Total = ' + self.currency+'%.2f' % total)
        return lines

    #Adding prices from an external source to our price list, the system currently supports CSV, JSON, and SQL
    def import_prices(self, file_type: str, file_path: str):
        
        #Attempt to read the file
        #if the data can't be read it's likely either the file_path is wrong 
        #or there is a mismatch between the file type and declared file type
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
                #TODO Assumed the data base would have a products table with product_code and price attributes
                #should eventually be updated to either be more robust 
                #or changed to actual production database standard (if necessary)  
                query = 'SELECT product_code, price FROM products'
                data = pd.read_sql_query(query,db)
            except:
                print(file_err)

        else:
            print("Unsupported file type")
            return

        #Assigned names to dataframe collums for standardisation, just in case the file contents result in weird column names
        data.columns=['product_code','price']
        #Index is not used here, but iterrows() returns a tuple
        for index,row in data.iterrows():
            product_code = row['product_code']
            price = row['price']
            self._price_list[product_code] = price
    
    #Method for changing the currency of the shopping cart
    def set_currency(self, currency: str):
        self.currency = currency