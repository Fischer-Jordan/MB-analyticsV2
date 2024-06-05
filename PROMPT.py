import openai
from openai import OpenAI
import json
import requests
from bs4 import BeautifulSoup
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from googleapiclient.discovery import build
from urllib.parse import urlparse
from fuzzywuzzy import fuzz, process


#pip3 install fuzzywuzzy
#pip install google-api-python-client




def calculate_cosine_similarity(str1, str2):
    vectorizer = CountVectorizer().fit_transform([str1, str2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

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
api_key = "sk-proj-s1k0b50RS7MryE6rY8seT3BlbkFJxA3KLxO2ItqvZ0wSsvUl"
client = OpenAI(api_key=api_key)
# api_key = "sk-proj-s1k0b50RS7MryE6rY8seT3BlbkFJxA3KLxO2ItqvZ0wSsvUl"
# client = OpenAI(api_key=api_key)

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


SEARCH_API_KEY='AIzaSyCvspkLbBiktJNh_Sbl1zexGy85VFmeKSU'
SEARCH_ENGINE_ID='d101fb0359f9d45d9'

def filter_links(links, vendor_name, item_name):
    """
    Filters the given links based on their relevance to the vendor_name and item_name.
    """
    top_link = None
    highest_ratio = 0
    for link in links:
        link_domain = urlparse(link).netloc
        domain_ratio = fuzz.partial_ratio(vendor_name.lower(), link_domain.lower())
        if domain_ratio < 50:
            continue
        match = re.search(r"https?://[^/]+(/.*)", link)
        if match:
            path = match.group(1)[1:]
            cleaned_path = " ".join(path.split("/"))
            item_ratio = fuzz.partial_ratio(item_name.lower(), cleaned_path.lower())
            ratio = (0.7 * domain_ratio) + (0.3 * item_ratio)
            if ratio > highest_ratio:
                highest_ratio = ratio
                top_link = link
    return top_link
    

def google_search(query, num_results=5):
    """
    Performs a Google search for the given query and returns the first link. I'll give you item name, brand name and vendor name.
    Return the link that'll take me to that particular item of that specific brand in the vendor website. 
    For example, if item is 'shoes', brand is 'Nike' and vendor is 'Amazon', give me a link that'll take me to the Nike shoes page in Amazon.com
    
    
    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to return. Default is 5.
        
    Returns:
        list: A list of URLs for the search results.
    """
    service = build("customsearch", "v1", developerKey=SEARCH_API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
    
    links = []
    if 'items' in result:
        for item in result['items']:
            links.append(item['link'])
    return links


def get_item_link(item, vendor, brand, seller, category):
    if category.lower() in ['restaurants', 'food', 'professional services' ,'charity']:
        print(f'yes i am from category {category}')
        query = f"{brand} {vendor} {category} location"
    else:
        query = f"buy {item} from {vendor} where brand is {brand}"
    return filter_links(google_search(query), vendor, item)


def get_json_from_text(text):
    """Get JSON from text using the openai API."""
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
                                            "description": "You need to extract the brand of the particular item. \
                                            \
                                            Brand name is NEVER similar\
                                            to item name. Brand name and item name should be completely different. If you think that the item name\
                                            is kinda similar to brand name, then change brand name to seller name. While going through the item name\
                                            check if the item name is preceeded by any Proper noun. Example: 'Panasonic TV' or 'Britannia cake'\
                                            here, TV is common noun, but Panasonic is Proper noun, so brand is Panasonic. Similarly, brand is Britannia\
                                            suppose the item is simply 'Shoes' or 'Organic sprouted pumpkin seeds', then do NOT assign item name as brand name\
                                            instead, look for its seller or vendor name and assign seller or vendor name as brand name. \
                                            Example: Vendor-> Nike, Seller-> Nike, Item: Shoes. Here brand is also Nike. \
                                             1. Look for capitalized words: Brands are often proper nouns, starting with capital letters. Identify potential brand names by recognizing capitalized words.\
                                            2. Consider company names: Check the header, remarks, or company details for a company name, as it might represent the brand.\
                                            3. Utilize known lists: Maintain a list of known brand names for recognition. Cross-reference the text with this list and consider matches as potential brands.\
                                            4. Observe patterns and indicators: Be attentive to specific patterns like 'Pvt Ltd,' 'Inc,' or 'LLC,' which often indicate company structures and may suggest a brand name.\
                                            5. Contextual information: Consider the context of the text. If there's a proper noun before an item name, it is likely the brand.\
                                            6. Default to vendor name: If no distinct brand is identified, default to the vendor name. In some cases, the vendor may also be the brand.\
                                            Examples:\
                                            1) 'Vendor: Amazon, Seller: 'Cake shop LTD.', Item: Britannia Cake' → Brand: Britannia (Proper noun present). \
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
            model="gpt-4-0125-preview",
            messages=messages,
            tools=tools,
        )
        
    except Exception as e:
        raise Exception("Openai API error. Please try again later.")
    
    # Step 2: check if GPT wanted to call a function
    if response.choices[0].message.tool_calls[0].function:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return None

 

def print_invoice_details(text):
    data = get_json_from_text(text)
    
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
    if(data.get('discount_amount')):
        print(f"Discount: ${float(data.get('discount_amount', 0.00)):.2f}")
    print(f"Total Amount: ${data.get('total_amount', 0.00):.2f}")
    print(f"Category: {category}")
    print()

    print("Vendor Details:")
    vendor_name=data.get('vendor_name', '')
    vendor_email=data.get('vendor_email', '')
    vendor_website=data.get('vendor_website')
    if data.get('vendor_website')=='' or not data.get('vendor_website'):
        vendor_website=extract_vendor_website(vendor_email)
    print(f"Vendor Name: {vendor_name}")
    print(f"Vendor Address: {data.get('vendor_address', '')}")
    print(f"Vendor Email: {vendor_email}")
    print(f"Vendor Website: {vendor_website}")
    print()
    print()

    
    print("Item Details:")
    for item in data.get('item', []):   
        item_name=item.get('name', '')
        item_category=item.get('item_category', 'Other')
        seller_name=item.get('seller_name', vendor_name)
        brand_name=item.get('brand', seller_name)
        item_link=item_link = get_item_link(item_name, vendor_name, brand_name,seller_name, category) 
        seller_email=item.get('seller_email', vendor_email)    
        similarity_score = calculate_cosine_similarity(brand_name.lower(), item_name.lower())
        threshold = 0.7
        print('similarity score: ', similarity_score)
        if similarity_score > threshold:
            brand_name = seller_name
        if category in ["Restaurants", "Entertainment","Grocery Stores and Supermarkets"]:
            brand_name = seller_name  
        print(f"Item Name: {item_name}")
        print(f"Item Category: {item_category}")
        print(f"Item Link: {item_link}")
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
        similarity_score = calculate_cosine_similarity(brand_name.lower(), item_name.lower())
        threshold = 0.7
        print('similarity score: ', similarity_score)
        if similarity_score > threshold:
            brand_name = seller_name
        if category in ["Restaurants", "Entertainment","Grocery Stores and Supermarkets"]:
            brand_name = seller_name 
        print(f"Brand Name: {brand_name}")
        print(f"Brand Address: {data.get('brand_address', '')}")
        print(f"Brand Phone: {data.get('brand_phone', '')}")
        print(f"Brand Email: {data.get('brand_email', '')}")
        print(f"Brand Website: {data.get('brand_website', '')}")
        print()




def get_page_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (like 404 Not Found)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    
    text="""
 > ---------- Original Message ----------> From: Swathi Mohan > To: FischerJordan Team , mybrands@fischerjordan.xyz> Date: 05/17/2024 7:34 PM IST> Subject: Fwd: Your receipt from LeetCode #2618-8278> > > > > ---------- Forwarded message ---------> From: LeetCode > Date: Mon, 4 Mar 2024 at 17:43> Subject: Your receipt from LeetCode #2618-8278> To: > > > > Your receipt from LeetCode #2618-8278 > > https://leetcode.com> LeetCode> > > > Receipt from LeetCode> $29.75> Paid March 4, 2024> > > > [invoice illustration]> Download invoice https://59.email.stripe.com/CL0/https:%2F%2Fpay.stripe.com%2Finvoice%2Facct_16Kf9YGo3RRcePD4%2Flive_YWNjdF8xNktmOVlHbzNSUmNlUEQ0LF9QZlczOUQxTGl4WjROR216OExZbk9hSmtEOUhGZFNuLDEwMDA5NTIxNA02004oX26W6t%2Fpdf%3Fs=em/1/0101018e09624761-794bb766-5ada-4fbb-9a47-abba01dd9d47-000000/wHniOHpDAk26qPsCc_-CafvYfXHX36CY0UqmGPARt_E=342 Download receipt https://59.email.stripe.com/CL0/https:%2F%2Fdashboard.stripe.com%2Freceipts%2Finvoices%2FCAcQARoXChVhY2N0XzE2S2Y5WUdvM1JSY2VQRDQo7vWWrwYyBtHVSSgG7zovFuGPnjKVUDrdP2AxuRenlKWYTQe9un9rIXKpmQnSy2me3OYPgsKEshC02tYa2ck%2Fpdf%3Fs=em/1/0101018e09624761-794bb766-5ada-4fbb-9a47-abba01dd9d47-000000/zMxOD6uKGoNBDWV7d5UrmGN7yGQSvusD1dbSCsqoLwU=342> > Receipt number 2618-8278> > Invoice number 3EB4B0D1-0003> > Payment method [Visa] - 3831> > > > > Receipt #2618-8278> > Mar 3 – Apr 3, 2024> > > Monthly Premium Subscription 2> > Qty 1> > $35.00> > > > Subtotal> > $35.00> > > > > > > India Monthly Discount - 2 (15% off)> > -$5.25> > > > > > > Total> > $29.75> > > > > > > Amount paid> > $29.75> > > > > > Questions? Visit our support site at https://leetcode.com/support/ or contact us at billing@leetcode.com mailto:billing@leetcode.com. > > > Powered by [stripe logo] https://59.email.stripe.com/CL0/https:%2F%2Fstripe.com/1/0101018e09624761-794bb766-5ada-4fbb-9a47-abba01dd9d47-000000/QHVTjSecmHhHUNel-ss2BeLY6dZZpoUIgIy87XSeRmI=342 | Learn more about Stripe Billing https://59.email.stripe.com/CL0/https:%2F%2Fstripe.com%2Fbilling/1/0101018e09624761-794bb766-5ada-4fbb-9a47-abba01dd9d47-000000/YGtryOjBV_LggquHsRmPXyP7bfpdPrvlvAYI_lUOalU=342> > > ---------- Original Message ---------- From: Swathi Mohan <swathi15mohan@gmail.com> To: FischerJordan Team <fischerjordan-team@fischerjordan.com>, mybrands@fischerjordan.xyz Date: 05/17/2024 7:34 PM IST Subject: Fwd: Your receipt from LeetCode #2618-8278 ---------- Forwarded message --------- From: LeetCode <invoice+statements+acct_16Kf9YGo3RRcePD4@stripe.com> Date: Mon, 4 Mar 2024 at 17:43 Subject: Your receipt from LeetCode #2618-8278 To: <swathi15mohan@gmail.com> Your receipt from LeetCode #2618-8278 LeetCode Receipt from LeetCode $29.75 Paid March 4, 2024 Download invoice Download receipt Receipt number 2618-8278 Invoice number 3EB4B0D1-0003 Payment method - 3831 Receipt #2618-8278 Mar 3 – Apr 3, 2024 Monthly Premium Subscription 2 Qty 1 $35.00 Subtotal $35.00 India Monthly Discount - 2 (15% off) -$5.25 Total $29.75 Amount paid $29.75 Questions? Visit our support site at https://leetcode.com/support/ or contact us at billing@leetcode.com. Powered by | Learn more about Stripe Billing 
 

"""
    text1="""
From: NextLegal Services <noreply@nextlegal.com>
Date: Sat, May 25, 2024 at 3:30 PM
Subject: Invoice for Legal Services
To: <your.email@example.com>

Dear Client,

Thank you for choosing NextLegal Services. Please find the details of your invoice below:

**Invoice ID**: LEG456789
**Service Date**: May 24, 2024

**Description**:
- Consultation Fee: ₹5,000
- Document Review: ₹2,500

**Total Amount Paid**: ₹7,500

We appreciate your trust in our legal services. For any inquiries, please contact us at support@nextlegal.com.

Best regards,
NextLegal Services

Please do not reply to this email. For any assistance, email support@primelegal.com.
"""

    text2="""
From: Wanderlust Travel Agency <noreply@wanderlusttravel.com>
Date: Wed, May 22, 2024 at 12:00 PM
Subject: Receipt for Travel Booking
To: <your.email@example.com>

Dear Traveler,

Thank you for booking your travel with Wanderlust Travel Agency. Below are the details of your transaction:

**Transaction ID**: TRV456789
**Booking Date**: May 20, 2024

**Description**:
- Vacation Package to Bali: ₹75,000
- Travel Insurance: ₹3,500

**Total Amount Paid**: ₹78,500

We hope you have a wonderful trip. For any assistance, please contact us at support@wanderlusttravel.com.

Best regards,
Wanderlust Travel Agency

This is an automated message. Please do not reply. For any queries, email support@wanderlusttravel.com.

"""


    text3="""
From: Hope for All Foundation <noreply@hopeforall.org>
Date: Thu, May 16, 2024 at 2:45 PM
Subject: Donation Receipt
To: <your.email@example.com>

Dear Donor,

Thank you for your generous contribution to the Hope for All Foundation. Please find your donation receipt below:

**Donation ID**: DON654321
**Donation Date**: May 15, 2024

**Description**:
- General Donation: ₹5,000

**Total Amount Donated**: ₹5,000

Your support helps us continue our mission to provide aid and support to those in need. Thank you for making a difference.

Sincerely,
Hope for All Foundation

This is an automated message. Please do not reply. For any inquiries, email support@hopeforall.org.
"""

    text4="""
From: Elite Business Consulting <noreply@eliteconsulting.com>
Date: Tue, May 14, 2024 at 9:00 AM
Subject: Invoice for Consulting Services

Dear Customer,

Thank you for choosing Elite Business Consulting. Please find the details of your invoice below:

**Invoice ID**: INV123456
**Service Date**: May 10, 2024

**Description**:
- Business Strategy Consultation: ₹3,000
- Market Analysis: ₹2,000
- Financial Planning Session: ₹4,500

**Total Amount Paid**: ₹9,500

We appreciate your business and look forward to serving you again.

Best regards,
Elite Business Consulting

Please do not reply to this email. For any queries, contact support@eliteconsulting.com.

"""

    text5="""
Re testing---------- Forwarded message ---------From: Param Kapur Date: Wed, May 15, 2024 at 10:01 PMSubject: Fwd: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: Swathi Mohan , <mybrands@fischerjordan.xyz> Param Kapur FischerJordan+91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If youare not an intended recipient of this email, please immediately notify thesender by replying to this email, delete the message and any attachmentsfrom your account, and do not forward or otherwise distribute the messageor any attachments.---------- Forwarded message ---------From: Param Kapur Date: Tue, May 14, 2024 at 22:02Subject: Fwd: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: ---------- Forwarded message ---------From: Goibibo Date: Tue, 14 May 2024 at 11:21Subject: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: Important update [image: Goibibo]Dear param "",Please find attached the Invoice for your Flight booking(GOFLDNTIJSEBZQ3C1456) with Goibibo on May 14, 2024. *( Your Invoice is nota valid travel document )*.For all further details, please visit MyTrips.Regards,*Team Goibibo*P.S.: This is a system generated email. Please do not reply to this email.Re testing ---------- Forwarded message ---------From: Param Kapur <param.kapur@fischerjordan.com>Date: Wed, May 15, 2024 at 10:01 PMSubject: Fwd: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: Swathi Mohan <swathi.mohan@fischerjordan.com>, <mybrands@fischerjordan.xyz> Param Kapur FischerJordan +91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If you are not an intended recipient of this email, please immediately notify the sender by replying to this email, delete the message and any attachments from your account, and do not forward or otherwise distribute the message or any attachments.---------- Forwarded message ---------From: Param Kapur <paramkapur2002@gmail.com>Date: Tue, May 14, 2024 at 22:02Subject: Fwd: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: <param.kapur@fischerjordan.com>---------- Forwarded message ---------From: Goibibo <noreply@goibibo.com>Date: Tue, 14 May 2024 at 11:21Subject: Tax Invoice for your Flight Booking id GOFLDNTIJSEBZQ3C1456To: <paramkapur2002@gmail.com>Important updateDear param "",Please find attached the Invoice for your Flight booking (GOFLDNTIJSEBZQ3C1456) with Goibibo on May 14, 2024. ( Your Invoice is not a valid travel document ).For all further details, please visit MyTrips.Regards,Team GoibiboP.S.: This is a system generated email. Please do not reply to this email.
     
"""
    text6="""
Cross verifying---------- Forwarded message ---------From: Param Kapur Date: Wed, May 15, 2024 at 10:00 PMSubject: Fwd: [Personal] Your Sunday afternoon trip with UberTo: Swathi Mohan , <mybrands@fischerjordan.xyz> Param Kapur FischerJordan+91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If youare not an intended recipient of this email, please immediately notify thesender by replying to this email, delete the message and any attachmentsfrom your account, and do not forward or otherwise distribute the messageor any attachments.---------- Forwarded message ---------From: Param Kapur Date: Tue, May 14, 2024 at 22:02Subject: Fwd: [Personal] Your Sunday afternoon trip with UberTo: ---------- Forwarded message ---------From: Uber Receipts Date: Sun, 12 May 2024 at 15:00Subject: [Personal] Your Sunday afternoon trip with UberTo: Total ₹715.61May 12, 2024Thanks for riding, ParamWe hope you enjoyed your ride this afternoon.Total ₹715.61You have an unfinished payment. Please review and pay nowTrip Charge ₹592.32Subtotal ₹592.32Wait Time₹0.65Pickup charges ₹160.30Promotion -₹37.66PaymentsPhonePe5/12/24 2:59 PM₹715.61FailedVisit the trip pagefor more information, including invoices (where available)The total of ₹715.61 has a GST of ₹61.20 included.Switch Payment MethodDownload PDFYou rode with ABUR4.86 RatingRate or tipLicense Plate: WB25H6421Premier21.66 kilometers | 39 min2:20 PM33, International Airport, Dum Dum, Kolkata, North Dumdum, West Bengal700052, India2:59 PM57H, Ballygunge Circular Rd, Ballygunge, Kolkata, West Bengal 700019, IndiaReport lost item ❯Contact support❯Contact support ❯My trips ❯Forgot passwordPrivacyTermsUber India Systems Private LimitedFares are inclusive of GST. Please download the tax invoice from the tripdetail page for a full tax breakdown.Cross verifying ---------- Forwarded message ---------From: Param Kapur <param.kapur@fischerjordan.com>Date: Wed, May 15, 2024 at 10:00 PMSubject: Fwd: [Personal] Your Sunday afternoon trip with UberTo: Swathi Mohan <swathi.mohan@fischerjordan.com>, <mybrands@fischerjordan.xyz> Param Kapur FischerJordan +91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If you are not an intended recipient of this email, please immediately notify the sender by replying to this email, delete the message and any attachments from your account, and do not forward or otherwise distribute the message or any attachments.---------- Forwarded message ---------From: Param Kapur <paramkapur2002@gmail.com>Date: Tue, May 14, 2024 at 22:02Subject: Fwd: [Personal] Your Sunday afternoon trip with UberTo: <param.kapur@fischerjordan.com>---------- Forwarded message ---------From: Uber Receipts <noreply@uber.com>Date: Sun, 12 May 2024 at 15:00Subject: [Personal] Your Sunday afternoon trip with UberTo: <paramkapur2002@gmail.com> Total₹715.61May 12, 2024 Thanks for riding, ParamWe hope you enjoyed your ride this afternoon. Total₹715.61You have an unfinished payment. Please review and pay now Trip Charge₹592.32 Subtotal₹592.32Wait Time₹0.65Pickup charges₹160.30Promotion-₹37.66 Payments PhonePe5/12/24 2:59 PM₹715.61FailedVisit the trip page for more information, including invoices (where available)The total of ₹715.61 has a GST of ₹61.20 included.Switch Payment MethodDownload PDF You rode with ABUR4.86RatingRate or tipLicense Plate: WB25H6421 Premier21.66 kilometers | 39 min2:20 PM33, International Airport, Dum Dum, Kolkata, North Dumdum, West Bengal 700052, India2:59 PM57H, Ballygunge Circular Rd, Ballygunge, Kolkata, West Bengal 700019, IndiaReport lost item ❯ Contact support❯Contact support ❯ My trips ❯ Forgot passwordPrivacyTermsUber India Systems Private Limited Fares are inclusive of GST. Please download the tax invoice from the trip detail page for a full tax breakdown."""


    # print_invoice_details(text)
    # print('---------------------------------------------------------------------------------------------------------')
    print_invoice_details(text1)
    print('---------------------------------------------------------------------------------------------------------')    
    # print_invoice_details(text2)
    # print('---------------------------------------------------------------------------------------------------------')    
    # print_invoice_details(text3)
    # print('---------------------------------------------------------------------------------------------------------')    
    # print_invoice_details(text4)
    # print('---------------------------------------------------------------------------------------------------------')    
    # print_invoice_details(text5)
    # print('---------------------------------------------------------------------------------------------------------')    
    # print_invoice_details(text6)
    # print('---------------------------------------------------------------------------------------------------------')    
