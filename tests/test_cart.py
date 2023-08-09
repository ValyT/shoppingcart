from shoppingcart.cart import ShoppingCart

#Basic cart functionality, price list access and receipt printing 
def test_add_item():

  cart = ShoppingCart()
  cart.add_item('apple', 1)

  receipt = cart.print_receipt()

  assert receipt[0] == 'apple - 1 - €1.00'

  

#Price calculation with quantity
def test_add_item_with_multiple_quantity():

  cart = ShoppingCart()
  cart.add_item('apple', 2)

  receipt = cart.print_receipt()

  assert receipt[0] == 'apple - 2 - €2.00'

  

#Item ordered on receipt same as input order
def test_item_order():

  cart = ShoppingCart()
  #Multiple items decrease chance input and receipt order allign accidentally
  cart.add_item('banana', 1)
  cart.add_item('kiwi', 1)
  cart.add_item('apple', 1)
  
  receipt = cart.print_receipt()
  assert receipt[0] == 'banana - 1 - €1.10'
  assert receipt[1] == 'kiwi - 1 - €3.00'
  assert receipt[2] == 'apple - 1 - €1.00'

#Total correctly calculated and added to receipt
def test_total():

  cart = ShoppingCart()
  cart.add_item('banana', 1)
  cart.add_item('kiwi', 1)
  cart.add_item('apple', 1)
  
  receipt = cart.print_receipt()
  assert receipt[0] == 'banana - 1 - €1.10'
  assert receipt[1] == 'kiwi - 1 - €3.00'
  assert receipt[2] == 'apple - 1 - €1.00'
  assert receipt[3] == 'Total = €5.10'

#Price import for non-sql formats
def test_price_import_non_sql():

  cart = ShoppingCart()

  cart.import_prices('csv', './prices.csv')
  cart.import_prices('json', './prices.json')
  
  cart.add_item('csv_product', 1)
  cart.add_item('json_product', 1)

  receipt = cart.print_receipt()
  assert receipt[0] == 'csv_product - 1 - €2.00'
  assert receipt[1] == 'json_product - 1 - €2.50'

#Price import for sql
def test_price_import_sql():

  cart = ShoppingCart()

  cart.import_prices('sql', './prices.db')

  cart.add_item('sql_product', 1)

  receipt = cart.print_receipt()
  assert receipt[0] == 'sql_product - 1 - €2.55'

#Price import for wrong format
def test_price_import_wrong_format():

  cart = ShoppingCart()

  cart.import_prices('csv', './prices.db')

  cart.add_item('sql_product', 1)

  receipt = cart.print_receipt()
  assert receipt[0] == 'sql_product - 1 - €2.55'

#Price import for unsupported format
def test_price_import_fake_format():

  cart = ShoppingCart()

  cart.import_prices('wrong_format', './prices.db')

  cart.add_item('sql_product', 1)

  receipt = cart.print_receipt()
  assert receipt[0] == 'csv_product - 1 - €2.55'

#Item not in price list handling
def test_add_non_existant():

  cart = ShoppingCart()
  cart.add_item('non_existant', 1)

  receipt = cart.print_receipt()

  assert receipt[0] == 'non_existant - 1 - €0.00'

#Displaying the price in a different currency
def test_currency_change():
  
  cart.set_currrency('$')
  
  cart = ShoppingCart()
  cart.add_item('apple', 1)

  receipt = cart.print_receipt()

  assert receipt[0] == 'apple - 1 - $1.00'