purchase_data=\
{'id': 531, 'purchase_items': [{'id': 1017, 'item': {'id': 475, 'brand': {'id': 259, 'name': 'Tahini by Enoki', 'website': ''}, 'name': 'Spicy Chicken Shawarma', 'sku_code': '996331', 'description': ' ', 'category': 'Restaurants'}, 'is_shared': False, 'quantity': 1.0, 'unit_price': 525.0, 'total_price': 525.0, 'seller_name': 'Tahini by Enoki', 'seller_website': '', 'purchase': 531}, {'id': 1018, 'item': {'id': 476, 'brand': {'id': 259, 'name': 'Tahini by Enoki', 'website': ''}, 'name': 'Spinach & Cheese Sambousek (4 Pcs)', 'sku_code': '996331', 'description': ' ', 'category': 'Restaurants'}, 'is_shared': False, 'quantity': 1.0, 'unit_price': 395.0, 'total_price': 395.0, 'seller_name': 'Tahini by Enoki', 'seller_website': '', 'purchase': 531}, {'id': 1019, 'item': {'id': 477, 'brand': {'id': 259, 'name': 'Tahini by Enoki', 'website': ''}, 'name': 'Classic Falafel Shawarma', 'sku_code': '996331', 'description': ' ', 'category': 'Restaurants'}, 'is_shared': False, 'quantity': 2.0, 'unit_price': 425.0, 'total_price': 850.0, 'seller_name': 'Tahini by Enoki', 'seller_website': '', 'purchase': 531}, {'id': 1020, 'item': {'id': 478, 'brand': {'id': 259, 'name': 'Tahini by Enoki', 'website': ''}, 'name': 'Lamb Adana Kebab', 'sku_code': '996331', 'description': ' ', 'category': 'Restaurants'}, 'is_shared': False, 'quantity': 1.0, 'unit_price': 475.0, 'total_price': 475.0, 'seller_name': 'Tahini by Enoki', 'seller_website': '', 'purchase': 531}], 'vendor': [{'id': 123, 'name': 'Zomato'}], 'category': {'id': 62, 'name': 'Restaurants'}, 'purchase_items_string': 'Spicy Chicken Shawarma (1.0) ,Spinach & Cheese Sambousek (4 Pcs) (1.0) ,Classic Falafel Shawarma (2.0) ,Lamb Adana Kebab (1.0) ', 'payee_name': 'Param Kapur', 'total_amount': 2533.65, 'date': '2024-02-04T00:00:00-05:00'}















for item in purchase_data['purchase_items']:
    brand_name = item['item']['brand']['name']
    product_name = item['item']['name']
    seller_name=item['seller_name']
    print('Brand Name:', brand_name)
    print('Product Name:', product_name)
    print('Seller Name:', seller_name)
        
if purchase_data['vendor']:
    vendor_name = purchase_data["vendor"][0]["name"]        
    print('Vendor Name:', vendor_name)

if purchase_data['category']:
        category_name = purchase_data['category']['name']
        print('Category Name:', category_name)

if purchase_data['payee_name']:
    payee_name = purchase_data['payee_name']
    print('Payee Name:', payee_name)

if purchase_data['total_amount']:
    print('Total amount: ', purchase_data['total_amount'])