

from openai import OpenAI
import json
import requests
from bs4 import BeautifulSoup
import os
import csv

api_key = "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"
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
count=0
def process_email(text, failure_count, success_writer):
    try:
        data = get_json_from_text(text)
        success_writer.writerow({'Email Text': text, 'Output': json.dumps(data)})
    except Exception as e:
        failure_count[0] += 1
        print(f"Error processing email: {failure_count[0]}")

        

def get_json_from_text(text):
    """Get JSON from text using the OpenAI API."""
    messages = [{
        "role": "user",
        "content": f"Email plain text content: {text}."
    }]
    tools = [
        {
            "type": "function",
            "function": {
                    "name": "parse_email_invoice",
                    "description": "Provided plain text content of an email invoice, return a JSON object that represents the invoice. Extract the brand and vendor accurately. Remember that a vendor is the same for all items, but each\
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

                            "vendor_website": {"type": "string", "description": "The website of the vendor.\
                                For example: www.walmart.com"},
                            

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
                                        capitalized."},
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
                                            brand name as the seller name, and not the item name." 
                                
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
                                            "description": "The name of the item. For example: 'Apple', 'Banana', 'Shoes', 'Laptop'. Most times, this is a\
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
    except Exception as e:
        raise Exception("OpenAI API error. Please try again later.")
    
    # Step 2: check if GPT wanted to call a function
    if response.choices[0].message.tool_calls[0].function:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return None

def main():
    input_csv_path = 'spam4.csv'
    output_csv_path = 'output.csv'
    failure_count = [0]
    

    with open(input_csv_path, 'r') as input_csv, open(output_csv_path, 'w', newline='') as output_csv:
        fieldnames = ['Email Text', 'Output']
        success_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        success_writer.writeheader()

        reader = csv.reader(input_csv)
        next(reader)  # Skip header row if it exists

        for row in reader:
            email_text = row[0]  # Assuming email text is in the first column
            process_email(email_text, failure_count, success_writer)

    print(f"Number of failed emails: {failure_count[0]}")

if __name__ == "__main__":
    main()

    
      

   