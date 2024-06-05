from openai import OpenAI
import json 
import os
from paddleocr import PaddleOCR
import time
ocr = PaddleOCR(lang='en') 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variable

img_path = 'receipt5.jpg'
stocr=time.time()
result = ocr.ocr(img_path, cls=False)
etocr=time.time()
for line in result:
        boxes = [item[0] for item in line]
        txts = [item[1][0] for item in line]
        scores = [item[1][1] for item in line]


api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)

product_categories = [
    "Airlines",
    "Appliances",
    "Art & Craft Supplies",
    "Books",
    "Cable",
    "Car Rental",
    "Cell & Phone",
    "Charity",
    "Consumer Electronics",
    "Dealerships",
    "Entertainment",
    "Financial Services",
    "Garden & Outdoor",
    "General Home Contracting",
    "Grocery Stores and Supermarkets",
    "Health and Fitness",
    "Home Supply Warehouse",
    "Hotels & Accommodations",
    "Jewelry, Watches, and Silverware",
    "Mail & Freight",
    "Media",
    "Medical & Dental",
    "Music Stores and Instruments",
    "Office Products",
    "Other",
    "Personal Services",
    "Pet Care & Supplies",
    "Professional Services",
    "Public Transportation",
    "Restaurants",
    "Retail",
    "Sporting Goods",
    "Travel - Other",
    "Utilities"
]
categories_with_subcategories = [
    "Air Travel",
    "Kitchen Appliances",
    "Art Supplies",
    "Novels & Literature",
    "Internet Services",
    "Vehicle Rentals",
    "Telecommunications",
    "Donations",
    "Gadgets",
    "Automotive Dealers",
    "Movies & Shows",
    "Banking & Investments",
    "Gardening Tools",
    "Home Renovation",
    "Supermarket Purchases",
    "Gym Memberships",
    "Home Maintenance",
    "Lodging",
    "Jewelry & Accessories",
    "Shipping Services",
    "Media Subscriptions",
    "Healthcare Services",
    "Musical Instruments",
    "Office Supplies",
    "Miscellaneous",
    "Personal Care",
    "Pet Care",
    "Legal & Consultancy",
    "Public Transport",
    "Dining Out",
    "Retail Purchases",
    "Sports Equipment",
    "Travel Packages",
    "Utilities",
    "Dairy Products",
    "Fresh Produce",
    "Bakery Items",
    "Frozen Items",
    "Beverages",
    "Snack Items",
    "Canned Foods",
    "Spices & Seasonings",
    "Meat & Seafood",
    "Breakfast Items",
    "Pasta & Grains",
    "Footwear",
    "Outdoor Gear",
    "Toys & Games",
    "Stationery & Writing",
    "Travel Accessories",
    "Household Appliances",
    "Apparel & Accessories"
]

def extract_vendor_website(email):
    domain_part = email.split('@')[-1]
    parts = domain_part.split('.')
    if len(parts) >= 2:
        vendor_name = parts[-2]
        com_part = parts[-1]
        vendor_website = f'www.{vendor_name}.{com_part}'
        return vendor_website
    else:
        return None  


def get_json_from_text(text, boxes):
    """Get JSON from text using the OpenAI API."""
    messages = [{
        "role": "user",
        "content": f"Focus on extracting the vendor name, item names, item prices, and quantities. If you don't get a lot of text, just\
                    focus on the text and boxes you've received and try to extract info from there. Do not throw OPENAI error.\
                    Correct all spelling mistakes. If item is spelled as 'Mjesli', correct it to 'Muesli', Similarly if it's 'DAR CHOCOLATE'\
                    correct it to 'DARK CHOCOLATE'. Do not use the text blindly. Always check for spelling mistakes.\
                    Receipt text content: {text}. Use the box coordinates {boxes} to identify relationships between texts. \
                    Consider side-by-side boxes as related (e.g., item and price), and vertically aligned boxes as \
                    continuous information (e.g., part of an address)."
    }]
    tools = [
        {
            "type": "function",
            "function": {
                    "name": "parse_receipt_data",
                    "description": "Provided plain text content of a receipt and the corresponding bounding boxes of each word\
                    , return a JSON object that represents the receipt. Extract the brand and vendor accurately. Remember that a vendor is the same for all items, but each\
                        item's brand might differ. So accordingly extract the vendor and correct brand for every item. For example: items: HP laptop, Britannia bread. Extract Vendor: 'Amazon', brand: 'HP',\
                        brand: 'Britannia.'",
                    "parameters": {
                        "type": "object",

                        "properties": {
                            "invoice_id": {
                                "type": "string",
                                "description": "The invoice ID. For example: '3245921', '#AD-1234'."
                            },
                            "payee_name": {
                                "type": "string",
                                "description": "The name of the person or company to whom the invoice is addressed to. \
                                For example: 'John Smith', 'Jane Doe', 'Anthony Mavromatis', Ensure to differentiate between brand or vendor name from Person name. Person's name often has \
                                first name and surname. Sometimes it's accompanies by texts like: 'Hi Boaz, this is your receipt.' You can also extract the name from the email\
                                address that the mail is addressed to"
                            },
                            "payee_address": {
                                "type": "string",
                                "description": "The home or company or work address of the  person or company to whom the invoice is addressed to. \
                                    This will usually be under a heading like 'Billing Address' or 'Shipping Address'. If \
                                    there is no address like this leave empty. \
                                    For example: '410 Terry Ave N, Seattle, WA 98109'"
                            },
                            "payee_phone": {
                                "type": "string",
                                "description": "The phone number of the  person or company to whom the \
                                    invoice is addressed to. For example: '1-800-123-4567'. If you see a 10 digit number, there's a good chance it's a phone number"
                            },
                            "payee_email": {
                                "type": "string",
                                "description": "The email address of the  person or company to whom the \
                                    invoice is addressed to. For example: 'john@gmail.com'"
                            },

                            "payment_method": {
                                "type": "string",
                                "description": "The payment method used to pay the invoice. \
                                    For example: 'Credit Card', 'PayPal'",
                                "enum": ["Credit Card", "PayPal", "Venmo", "Cash", "Check", "Debit Card", "Crypto"]
                            },
                            "payment_method_detail": {
                                "type": "string",
                                "description": "The payment method details used to pay the invoice. \
                                    For example: 'Visa ending in 1234', 'PayPal account: #7628'"
                            },
                            "vendor_name": {"type": "string", 
                                "description": "To extract the vendor name, simply look at the FROM line in the email. Just look for the sender of the email. If the email\
                                is sent by noreply@amazon.com, simply pick the proper nound from this sender email which is Amazon.Remember to remove the '@' and '.com' \
                                from the email and only retain the proper noun like 'amazon'. That'll be the vendor.\
                                some other examples are: no-reply@status.vons.com, updates@myntra.com etc. Just pick the proper nouns like Vons, Myntra. Basically, just\
                                parse the From text and extract the vendor from there."},
                            
                            "vendor_email": {"type": "string", 
                                "description": "To extract the vendor email, simply look at the FROM line in the email. Just look for the sender of the email. \
                                If the email\
                                is sent by noreply@amazon.com, the vendor email is Amazon.\
                                some other examples are: no-reply@status.vons.com, updates@myntra.com etc."},
                            
                            "vendor_address": {"type": "string", 
                                "description": "Now that you have the vendor name, just find any address that has the vendor in it. For example\
                                if vendor is Amazon, find the address of Amazon- like: 'Amazon, 410 Terry Ave N, Seattle, WA 98109'"
                                },
                            "vendor_phone": {"type": "string", "description": "The Phone of the vendor.\
                                For example: www.walmart.com"},

                            "vendor_website": {"type": "string", "description": "The website of the vendor. This can be extracted from vendor email\
                                So, simply look at the FROM line in the email. Just look for the sender of the email. \
                                If the email is sent by noreply@amazon.com, then vendor website can be created like this:\
                                First extract the word just before '.com' and '.com'. For the email noreply@amazon.com, that is \
                                amazon and .com. Now append 'www.' in the beginning. The vendor website is constructed as 'www.amazon.com'\
                                some other examples are: no-reply@status.vons.com: vendor website is www.vons.com, updates@myntra.com: vendor \
                                website is www.myntra.com etc."         
                                },
                            

                            "item": {
                                "type": "array",
                                "description": "The item on the invoice.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "seller_name": {"type": "string", "description": "This is the name of the seller that's selling a particular item. It's often the name of the \
                                        shop, or name of the restaurant etc. If it's a shop, it's often followed by Pvt Ltd. or Ltd. or private Limited or Limited etc. \
                                        Sometimes it's the same as the vendor. For each item, look at the 'Sold by' data. It's ofen sold by a particular shop \
                                        or restaurant or a theatre etc. If you find a proper noun that is not the Vendor, check if it can be the seller.\
                                        So only pick the seller and populate it here. Another hint is that first letter of Seller name will be \
                                        capitalized. Fix the spelling mistakes yourself"},
                                        "seller_address": {"type": "string", "description": "The address of the seller.\
                                            For example: '410 Terry Ave N, Seattle, WA 98109'"},
                                        "seller_phone": {"type": "string", "description": "The phone number of the seller.\
                                            For example: '1-800-123-4567'"},
                                        "seller_email": {"type": "string", "description": "The email address of the seller.\
                                            For example: contact@walmart.com"},
                                        "seller_website": {"type": "string", "description": "The website of the seller.\
                                            For example: www.walmart.com"},
                                        "brand": {
                                            "type": "string",
                                            "description": "Extract brand names from invoices with these rules: Default to the vendor name if no distinct brand \
                                            \is identified, ensuring the brand field is always filled. Look for the company name in the header or 'Remarks'. \
                                            Notice patterns like 'Pvt Ltd', 'Inc', or 'LLC', and capitalized words, which often indicate brands. \
                                            Use known lists for recognition and adjust based on feedback. \
                                            Examples: 1) 'Vendor: Amazon, Seller: 'Cake shop LTD.', Item: Britannia Cake' → Brand: Britannia (Proper noun present). \
                                            2) 'Vendor: Nike, Seller: 'Nike', Item: Shoes' → Brand: Nike (No proper noun; default to vendor). \
                                            Always prioritize distinct brand names over vendor names when available. While dealing with restaurants, always put \
                                            brand name as the seller name, and not the item name.Fix the spelling mistakes yourself" 
                                
                                            },                                  
                                        
                                        "brand_address": {"type": "string", "description": "The address of the brand. Do not confuse it with the address of the vendor\
                                        unless the brand and vendor are the same. Ensure that if the brand and vendor are the same, all the brand details are exactly \
                                            the same as vendor details\
                                        For example: '410 Terry Ave N, Seattle, WA 98109'"},
                                        "brand_phone": {"type": "string", "description": "The phone number of the brand.\Do not confuse it with the phone of the vendor\
                                        unless the brand and vendor are the same.\Ensure that if the brand and vendor are the same, all the brand details are exactly \
                                            the same as vendor details\
                                            For example: '1-800-123-4567'"},
                                        "brand_email": {"type": "string", "description": "The email address of the brand.\Do not confuse it with the email of the vendor\
                                        unless the brand and vendor are the same.\Ensure that if the brand and vendor are the same, all the brand details are exactly \
                                            the same as vendor details\
                                            For example: contact@Britannia.com"},
                                        "brand_website": {"type": "string", "description": "The website of the brand.\Do not confuse it with the website of the vendor\
                                        unless the brand and vendor are the same.\Ensure that if the brand and vendor are the same, all the brand details are exactly \
                                            the same as vendor details\
                                            For example: www.nike.com"},

                                        "item_category":{
                                            "type":"string",
                                            "description":"This is the category for each item. Assign this category looking at the categories_with_subcategories\
                                            list provided to you. Ensure that every item category assigned is only from this list. Don't make up your own \
                                            categories. Example: Suppose the item is 'Shoes', then look at 'categories_with_subcategories' and assign\
                                            item_category as 'shoes'. Suppose item is a necklace, then item_category is Accessories.",
                                            "enum":categories_with_subcategories 
                                        },
                                            
                                        

                                        "name": {
                                            "type": "string",
                                            "description": "The name of the item. For example: 'Apple', 'Banana', 'Shoes', 'Laptop'.\
                                            Remember to fix the spelling mistakes. If the text is 'mjesli' it's probably 'Muesli'\
                                            Similarly if it's 'dkchcolate' it's probably 'dark chocolate.' Take such clever guesses and \
                                            do not make spelling mistakes.\
                                            So ensure to fix these mistakes yourself. Most times, item name is a\
                                            common noun. If there's a proper noun attached to it, it's probably the brand name.\
                                            Use this as a criteria to classify and extract only item name here.\
                                            Extract only the name of the item and not its brand."
                                        },
                                        "sku": {"type": "string", "description": "The SKU of the item. If there is no SKU,\
                                            this value should be null. For example: '1234-5678-9012'"},
                                        "quantity": {"type": "number", "description": "The quantity of the item."},
                                        "unit_price": {"type": "number", "description": "The unit price of the item in \
                                            the currency of the invoice."},
                                        "total_price": {"type": "number", "description": "The total price of the item in \
                                            the currency of the invoice."},
                                    },
                                },
                            },

                            "subtotal_amount": {"type": "number", "description": "The subtotal amount of the invoice."},
                            "tax_amount": {"type": "number", "description": "The tax amount of the invoice. \
                                If there is no tax, this value should be 0.00"},
                            "discount_amount": {"type": "number", "description": "The discount amount of the invoice. \
                                If there is no discount, this value should be 0.00"},
                            "shipping_amount": {"type": "number", "description": "The shipping amount of the invoice. \
                                If there is no shipping, this value should be 0.00"},
                            "total_amount": {"type": "number", "description": "The total amount of the invoice."},

                            "date": {
                                "type": "string",
                                "description": "The date of the invoice in the format of 'YYYY-MM-DD'.\
                                    For example: '2021-06-13'"
                            },
                            "category_name": {
                                "type": "string",
                                "description": "Assign a category for every transaction. Assign this category looking at the product_categories list provided\
                                to you. Ensure that every category assigned is only from this list. Don't make up your own categories.\
                                Look at the market place, the vendor and the brand to understand which category from the enum product_categories\
                                the transaction belongs to. Example: If market_place is 'Swiggy', Vendor is 'Dollops', and brand is 'Chicken roll' then \
                                the category is Restaurants as the transaction is regarding food. The default is Retail. So if you don't know a category, \
                                set it to 'Retail'",
                                "enum": product_categories
                            },
                        },
                         "required": ["invoice_id", "payee_name", "payee_email", "payee_address", 
                             "payee_phone", "vendor_name", "shipping_amount", "tax_amount", 
                             "discount", "total_amount", "source", "category", 
                             "vendor_address", "vendor_phone", "vendor_email", "vendor_website", 
                             "seller_name"
                             "seller_address", "seller_email", "seller_phone"
                             "seller_website","brand_name", "item_name", "sku_code", 
                             "description", "category_name", "item_category","brand_address", 
                             "brand_phone", "brand_email", "brand_website"],
                },
            },
        }
        
    ]
    try: 
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
        )
        print(response)
    except Exception as e:
        raise Exception("OpenAI API error. Please try again later.")
    
    # Step 2: check if GPT wanted to call a function
    if response.choices[0].message.tool_calls[0].function:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return None


def print_invoice_details(text, boxes):
    data = get_json_from_text(text, boxes)
    category=data.get('category_name', 'Other')

    """Print invoice details."""
    print("Purchase Details:")
    print(f"Invoice ID: {data.get('invoice_id', '')}")
    print(f"Payee Name: {data.get('payee_name', '')}")
    print(f"Payee Address: {data.get('payee_address', '')}")
    print(f"Payee Phone: {data.get('payee_phone', '')}")
    print(f"Payee Email: {data.get('payee_email', '')}")
    print(f"Vendor: {data.get('vendor_name', '')}")
    print(f"Shipping Amount: ${data.get('shipping_amount', 0.00):.2f}")
    print(f"Tax Amount: ${data.get('tax_amount', 0.00):.2f}")
    if data.get('discount_amount'):
        print(f"Discount: ${float(data.get('discount_amount', 0.00)):.2f}")
    print(f"Total Amount: ${data.get('total_amount', 0.00):.2f}")
    print(f"Category: {category}")
    print()

    print("Vendor Details:")
    vendor_name=data.get('vendor_name', '')
    vendor_email=data.get('vendor_email', '')
    if data.get('vendor_website')=='' or not data.get('vendor_website'):
        vendor_website=extract_vendor_website(vendor_email)
    else:
        vendor_website=data.get('vendor_website')
    print(f"Vendor Name: {vendor_name}")
    print(f"Vendor Address: {vendor_website}")
    print(f"Vendor Email: {vendor_email}")
    print(f"Vendor Website: {data.get('vendor_website', '')}")
    print()
    print()

    
    print("Item Details:")
    for item in data.get('item', []):
       
        item_name=item.get('name', '')
        item_category=item.get('item_category', 'Other')
        seller_name=item.get('seller_name', vendor_name)
        seller_email=item.get('seller_email', vendor_email)
        brand_name=item.get('brand', seller_name)
        if category in ["Restaurants", "Entertainment"]:
            brand_name = seller_name  
        print(f"Item Name: {item_name}")
        print(f"Item Category: {item_category}")
        print(f"Seller Name: {seller_name}")
        print(f"Seller Email: {seller_email}")
        print(f"Brand Name: {brand_name}")
        print(f"Quantity: {item.get('quantity', '')}")
        print(f"Unit Price: {item.get('unit_price', '')}")
        print(f"Total Price: {item.get('total_price', '')}")
        print(f"SKU Code: {item.get('sku', '')}")
        print()

    print("Brand Details:")
    for item in data.get('item', []):
        item_name=item.get('name', '')
        item_category=item.get('item_category', 'Other')
        seller_name=item.get('seller_name', vendor_name)
        seller_email=item.get('seller_email', vendor_email)
        brand_name=item.get('brand', seller_name)
        if category in ["Restaurants", "Entertainment"]:
            brand_name = seller_name 
        print(f"Brand Name: {brand_name}")
        print(f"Brand Address: {data.get('brand_address', '')}")
        print(f"Brand Phone: {data.get('brand_phone', '')}")
        print(f"Brand Email: {data.get('brand_email', '')}")
        print(f"Brand Website: {data.get('brand_website', '')}")
        print()





if __name__ == "__main__":
#     with open('texts.txt', 'r') as file:
#         text = file.read()
#     with open('boxes.txt', 'r') as file:
#         boxes = file.read()
    stllm=time.time()
    print_invoice_details(txts, boxes)
    etllm=time.time()
    print("OCR TIME: ", etocr-stocr)
    print("LLM TIME: ", etllm-stllm-18)

