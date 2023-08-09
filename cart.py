import typing

from . import abc
import queue

class ShoppingCart(abc.ShoppingCart):
    def __init__(self):
        self._items = dict()
        self._order = queue.Queue()

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

            price = self._get_product_price(product_code) * amount
            total+=price
            price_string = '€%.2f' % price

            lines.append(product_code + ' - ' + str(amount) + ' - ' + price_string)
        lines.append('Total = ' + '€%.2f' % total)
        return lines

    def _get_product_price(self, product_code: str) -> float:
        price = 0.0

        if product_code == 'apple':
            price = 1.0

        elif product_code == 'banana':
            price = 1.1

        elif product_code == 'kiwi':
            price = 3.0

        return price
