import json
import random

# def serialize_purchases_posts(posts):
#     extracted_data = []
#     for post in posts['data']:
#         for item in post['items']:
#             item_data = item['purchase_item']['item']
#             extracted_item = {
#                 'brand_name': item_data['brand']['name'],
#                 'item_name': item_data['name'],
#                                'sku_code': item_data.get('sku_code', ''),
#                 'description': item_data.get('description', ''),
#                 'category': item_data.get('category', ''),
#                 'quantity': item.get('quantity'),  # Use .get() method with a default value
#                 'unit_price': item.get('unit_price'),
#                 'total_price': item.get('total_price'),
#                 'seller_name': item.get('seller_name', ''),
#                 'likes_count': post.get('likes_count', 0),
#                 'author_name': post['author_detials'].get('name', ''),
#                 'author_email': post['author_detials'].get('email', ''),
#                 'caption': post.get('caption', ''),
#                 'url': post.get('url', ''),
#                 'price': post.get('price', ''),
#                 'date': post.get('date', ''),
#                 'user_id': post.get('user', '')
#             }
#             extracted_data.append({'purchase_history': extracted_item})
#     return extracted_data

def serialize_purchases_posts(posts):
    purchase_history_list = []
    for post in posts['data']:
        for item in post["items"]:
            purchase_history = {
                "item_name": item["purchase_item"]["item"]["name"],
                "item_category": item["purchase_item"]["item"]["category"],
                "brand_name": item["purchase_item"]["item"]["brand"]["name"] if item["purchase_item"]["item"]["brand"] else None,
                "unit_price": item["purchase_item"]["unit_price"],
                "total_price": item["purchase_item"]["total_price"],
                "quantity": item["purchase_item"]["quantity"],
                "seller_name": item["purchase_item"]["seller_name"],
                "date": item["date"],
                "vendor_name": post["vendor"]["name"],
                "author_name": post["author_detials"]["name"],
                "author_email": post["author_detials"]["email"],
                "brand_name_post": post["brand_name"],
                "item_name_post": post["item_name"],
                "url":post["url"],
                "price_post": post["price"],
                "date_post": post["date"],
                "user_id": post["user"]
            }
            purchase_history_list.append({'purchase_history': purchase_history})

    return purchase_history_list








with open('other_dump.json', 'r') as file:
    data = json.load(file)
modified_data=serialize_purchases_posts(data)
with open('other_dump.json', 'w') as file:
    json.dump(modified_data, file, indent=4)