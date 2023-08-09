from . import test_cart

#Basic cart functionality, price list access and receipt printing 
test_cart.test_add_item()

#Price calculation with quantity
test_cart.test_add_item_with_multiple_quantity()

#Item ordered on receipt same as input order
test_cart.test_item_order()

#Total correctly calculated and added to receipt
test_cart.test_total()

#Price import for non-sql formats
test_cart.test_price_import_non_sql()

#Price import for sql
test_cart.test_price_import_sql()

#Price import for wrong format
test_cart.test_price_import_wrong_format()

#Price import for unsupported format
test_cart.test_price_import_fake_format()

#Item not in price list handling
test_cart.test_add_non_existant()

#Displaying the price in a different currency
test_cart.test_currency_change()