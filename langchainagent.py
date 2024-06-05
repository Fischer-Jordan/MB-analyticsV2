   
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
import json
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from openai import OpenAI
import time
from groq import Groq






import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings


# class GroqOpenAIEmbeddings(GroqEmbeddings):
#     def embed_query(self, query):
#         return self.groq.embed(query)
#     def search(self, query):
#         return self.groq.search(query)
    
# class GroqVectorStore:
#     def __init__(self, api_key):
#         self.groq = Groq(api_key=api_key)
    

openai_api_key = "sk-proj-s1k0b50RS7MryE6rY8seT3BlbkFJxA3KLxO2ItqvZ0wSsvUl"
mytime = 0
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
# client = OpenAI(api_key=openai_api_key)
client = Groq(
    api_key="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",
)




class Transformer:

            def __init__(self, sys_msg: str, model=None, temperature=0):
                self.sys_msg = sys_msg
                self.model = model or "gpt-4-turbo-preview"
                #self.model = model or "gpt-3.5-turbo"
                self.temperature = temperature

            def __call__(self, usermsg: str) -> str:
                response = client.chat.completions.create(
                    temperature=self.temperature,
                    # model=self.model,
                    messages=[
                        {"role": "system", "content": self.sys_msg},
                        {"role": "user", "content": usermsg},
                    ],
                    model="mixtral-8x7b-32768",
                    #model="gpt-3.5-turbo",
                    response_format={ "type": "json_object" },
                    seed = 42
                )
                return response.choices[0].message.content

class QueryClassifier:
    sys_msg = """

The system has three primary data sources: my documents (containing purchase history of the mine only), \
other_user documents (containing purchase history of all other users except the given user), \
and a database (PostgreSQL database containing all purchase history and transactions).
You need to return an array of one or more categories that the query could fall in. Please note that if the category is 'my'\
or 'other_user', then langchain has to perform semantic analysis on that query and fetch 3 documents semantically closest to the query.\
So before categorizsing a query as 'my' or 'other_user', make sure that the query has keywords that would be useful for semantic analysis.

RULES FOR CLASSIFICATION:
1) If it contains common nouns that are semantically useful, the categorization is either 'My' or 'Other_user' or both or 'My and SQL'.
2) If there are no words useful for semantic search, then it could be SQL.

Keywords important/relevant for semantic analysis include:
common nouns like desktop, laptop, electronics, clothes, makeup, refrigerator, food, movies, fish, theatre, charger, tops, jeans,\
plants, nursery, school, office, garden etc
if the query makes a reference to any COMMON NOUN not limited to this, the category could either be user, other_user or both



1. My Category (Langchain Analysis):
   The Langchain semantic constraint is applied to queries that only need my transaction history. Langchain converts my info \
    into documents and employs semantic understanding to extract relevant information. 
    NOTE: My category should be chosen if the query has keywords for semantic analysis AND is solely based on my \
    transactions
    Here are 10 examples:
   1. "What are my favorite clothing brands?"  (keyword: clothing)
   2. "Which restaurants do I frequent the most?" (keyword: restaurants)
   3. "What type of books do I enjoy reading?" (keywordL books)
   5. "Which makeup products do I use regularly?" (keyword: makeup)
   6. "What cuisines do I prefer ordering?" 
   7. "What kind of movies do I watch the most?" 
   8. "Which grocery stores do I shop at frequently?" 
   9. "What genres of music do I listen to often?" 
   10. "What are my most purchased household items?" 


2. Other User Category (Langchain Analysis):
   Similarly, Langchain analyzes queries related to other users' experiences and preferences by converting other_user \
    info into Langchain documents. Note that reference to a particular user falls in this category. Here are 10 examples:
   1. "What are the most popular clothing brands among others?" (Here langchain will retrieve 3 docs semantically closest to clothing from OTHER user's transactions)
   2. "Which restaurants are highly rated by others?"
   3. "What are the preferred book genres among other users?"
   4. "Which electronics brands are commonly purchased by others?"
   5. "What makeup brands are trending among others?"
   6. "Which tiffin box is recommended for keeping food warm during travel?"
   7. "What are the must-have kitchen gadgets for a home chef?"
   8. "What's the best brand for noise-canceling headphones?"
   9. "What are the latest trends in smart home technology?"
   10. "What should I get Param for his birthday?"
   11. "What's the best cologne I can get from Amazon?"
   12. "Best place to buy seafood or fish?"


3. SQL Category (Database Query):
   IF AND ONLY IF THERE ARE ABSOLUTELY NO keywords that could be semantically useful, then category could be SQL. \
    If there's even a single keyword that could be semantically useful, the category SHOULD NOT be SQL. Here are 10 examples:
   1. "Which brand is purchased the most overall?" (no keyword)
   2. "What category of items is the most popular?" (no keyword)
   3. "What are the top-selling products this month?" (no keyword)
   4. "Which vendor has the highest sales volume?"
   5. "Which is my most purchased brand" (Here langchain would be meaningless as it would try to fetch documents semantically closest\
        to 'purchased' or 'brand' which is not right. Instead we need to query the database)
   6. "What category of items do I buy the most?"
   7. "What is my average spending per transaction?"
   8."What is the average shipping time for orders placed by others?"
   9."What is the average spending per transaction for others?"
       

4. My and Other User Categories (Mixed Langchain Analysis):
   Queries requiring analysis of both mine and other_user data sources. Langchain converts both mine and other_user info into Langchain documents. Here are 10 examples:
   1. "What brands of clothing are popular among others and me?"
   2. "Which restaurants are frequented by others and me the most?" (Semantic analysis to be performed on both user and other user's documents)
   3. "What types of books are enjoyed by others and me?"
   4. "What electronics brands are commonly owned by others and me?"
   5. "Which makeup products are commonly used by others and me?"
   6. "What cuisines are preferred by others and me?"
   7. "What movie genres are liked by others and me?"
   8. "Where do others and I usually shop for groceries?"
   9. "What music genres are listened to by others and me?"
   10. "What household items are frequently purchased by others and me?"
   
5. My and SQL (Langchain + SQL):
    These include queries requiring analysis of my documents and then a SQL query to be performed after fetching all of my \
    relevant documents.
    1. "how many times have I purchased clothes from Urbanic, what are they and how much have I spent on it in total?" \
    (keyword: '  Urbanic, clothes; SQL: total amount aggregrate )
    2. "How many times have I bought lipstick and how much have I spent on it?" (keyword: lipstick; SQL: total amount aggregrate)
    "How many times have I purchased dresses from Urbanic, and what is the minimum price I've paid for a dress?" (Keywords: Urbanic, dresses, minimum price)
    3. "What is the total amount spent on shoes purchased from Nike, and what is the average quantity purchased per transaction?" (Keywords: Nike, shoes; SQL: total amount, average quantity)
    4. "How many times have I bought t-shirts from Urbanic, and what is the sum of the prices for all t-shirts?" (Keywords: Urbanic, t-shirts; SQL: sum of prices)
    5. "How many times have I purchased jackets from Adidas, and what is the median price of all jackets?" (Keywords: Adidas, jackets; SQL: median price)
    6. "What is the maximum quantity of pizzas I've bought from Pizzahut or Dominos, and what is the total amount spent on them?" (Keywords: Pizzahut, pizza,Dominoes; SQL: maximum quantity, total amount)
    7. "What is the total quantity of socks I've purchased, and what is the standard deviation of prices for all socks?" (Keywords: socks; SQL: total quantity, standard deviation of prices)
        

   

   List of known categories:
   1. My
   2. Other_user
   3. SQL
   4. My and Other_user
   5. My and SQL

Your output should be a valid JSON object. Please strictly adhere to the following output:

{
    "category": [
        {
            "classification": "<categories identified>",
            "reason":"<reason for the classification>"
        }
    ]
}    




    """
    prompt = """
    {query}

    """
    def __init__(self, model=None):
        self.transform = Transformer(self.sys_msg, model=model)

    def __call__(self, query: str) -> str:
        return self.transform(self.prompt.format(query=query))
    

class SQLengineanddocs:
    sys_msg = """

Generate a sql query to be performed on postgrsql database. Give in django shell. I'll provide you 3 documents and all relevant schema.\
You need to first look at the documents and understand the category, vendor, item etc. After that look at the schema and \
generate a query. Dont simply jump to the schema and generate a random query. It's important to look at the documents and get \
information ONLY FROM THE DOCUMENTS. From the documents, understand what the categories are, what the item names are, what the vendors\
and brands are etc. 
LOOK AT THE DOCUMENTS AND UNDERSTAND EXACTLY WHAT THE SQL QUERY SHOULD BE LIKE. THIS IS VERY IMPORTANT. \

Approach:
1. Given 3-6 documents, first identify all the documents that could answer the question. For example, is user question is about makeup\
you might have 4 documents where 2 documents are makeup products and other 2 documents are irrelevant.
2. It's absolutely important to look at the purchase_item_string field or the item name field and pick the relevant documents.
3. Once you've identified the relevant documents, find one or more common fields.  In the above example, find what is common among the \
first 2 documents.
4. Generate SQL query according to the common fields that you've found
5. End the SQL query by grouping according to the given userID. Also make sure that the SQL query also returns the transaction IDs. \
The sql query should answer the question and also return all the relevant transaction IDs.
6. Also be careful not to go into extreme detail while generating the SQL query because our aim is to find all the transactions relevant\
to user query. So there might be more transactions than just what's mentioned in the documents.

Note: Do not return Item IDs. Return item names only. 

Schema:
i have a data_purchase table.
i also have tables like brand, category, vendor. but purchase is the most important table. \
Generate SQL queries keeping in mind the schema of purchase table as well as the 3 documents given to you.
DO NOT CHANGE THE NAME OF ANY TABLE.

data_brand:
- Fields:
  - name: CharField (max_length=255, unique=True)
  - logo: ImageField (upload_to="brand_logos/", blank=True, null=True)
  - parent_company: CharField (max_length=255, blank=True, null=True)
  - website: URLField (blank=True, null=True)
  - description: TextField (blank=True, null=True)
  - phone: CharField (max_length=255, blank=True, null=True)
  - email: EmailField (blank=True, null=True)
  - address: TextField (max_length=255, blank=True, null=True)
  - city: CharField (max_length=255, blank=True, null=True)
  - country: CharField (max_length=255, blank=True, null=True)
  - tax_id: CharField (max_length=255, blank=True, null=True)
  - tax_id_type: CharField (max_length=255, blank=True, null=True)
  - tax_id_country: CharField (max_length=255, blank=True, null=True)
  - tax_id_state: CharField (max_length=255, blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the brand

data_item:
- Fields:
  - brand: ForeignKey to Brand (on_delete=models.CASCADE, null=True, blank=True)
  - name: CharField (max_length=255, unique=True)
  - sku_code: CharField (max_length=255, null=True, blank=True)
  - description: TextField (null=True, blank=True)
  - category: CharField (max_length=255, null=True, blank=True)
- Properties:
  - brand_name: returns the name of the brand associated with the item
- Methods:
  - __str__: returns a string representation of the item

data_vendor:
- Fields:
  - name: CharField (max_length=255)
  - logo: ImageField (upload_to="vendor_logos/", blank=True, null=True)
  - website: URLField (blank=True, null=True)
  - description: TextField (blank=True, null=True)
  - phone: CharField (max_length=255, blank=True, null=True)
  - email: EmailField (blank=True, null=True)
  - address: TextField (max_length=255, blank=True, null=True)
  - city: CharField (max_length=255, blank=True, null=True)
  - country: CharField (max_length=255, blank=True, null=True)
  - tax_id: CharField (max_length=255, blank=True, null=True)
  - tax_id_type: CharField (max_length=255, blank=True, null=True)
  - tax_id_country: CharField (max_length=255, blank=True, null=True)
  - tax_id_state: CharField (max_length=255, blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the vendor

data_category:
- Fields:
  - name: CharField (max_length=255, unique=True)
- Methods:
  - __str__: returns a string representation of the category

data_purchaseItem:
- Fields:
  - item: ForeignKey to Item (on_delete=models.CASCADE)
  - purchase: ForeignKey to Purchase (on_delete=models.CASCADE)
  - quantity: FloatField (blank=True, null=True)
  - unit_price: FloatField (blank=True, null=True)  # in cents
  - total_price: FloatField (blank=True, null=True)  # in cents
  - is_favorite: BooleanField (default=False)
  - seller_name: CharField (max_length=255, blank=True, null=True)
  - seller_address: TextField (max_length=255, blank=True, null=True)
  - seller_email: EmailField (blank=True, null=True)
  - seller_phone: CharField (max_length=255, blank=True, null=True)
  - seller_website: URLField (blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the purchase item

data_purchase:
- Fields:
  - transaction_id: CharField (max_length=255)
  - user: ForeignKey to User (on_delete=models.CASCADE)
  - email_image_url: URLField (blank=True, null=True)
  - purchase_image: ImageField (upload_to="purchase_images/", blank=True, null=True)
  - payee_name: CharField (max_length=255, blank=True, null=True)
  - payee_address: TextField (max_length=255, blank=True, null=True)
  - payee_email: EmailField (blank=True, null=True)
  - payee_phone: CharField (max_length=255, blank=True, null=True)
  - vendor: ForeignKey to Vendor (on_delete=models.CASCADE)
  - category: ForeignKey to Category (on_delete=models.CASCADE, null=True, blank=True)
  - payment_method: CharField (max_length=255, blank=True, null=True)
  - last_four_digits: CharField (max_length=4, blank=True, null=True)
  - shipping_amount: FloatField (null=True, blank=True)
  - tax_amount: FloatField (null=True, blank=True)
  - discount_amount: FloatField (null=True, blank=True)
  - total_amount: FloatField
  - date: DateTimeField (default=timezone.now)
  - uploaded_at: DateTimeField (default=timezone.now)
  - is_edited: BooleanField (default=False)
  - edited_at: DateTimeField (blank=True, null=True)
  - note: TextField (blank=True, null=True)
  - source: CharField (max_length=255, choices=SOURCE_CHOICES, default=SOURCE_CHOICES[0][0])
  - raw_data: TextField (blank=True, null=True)
  - html_data: TextField (blank=True, null=True)
  - attachment: ForeignKey to EmailAttachments (on_delete=models.CASCADE, null=True, blank=True)
  - is_deleted: BooleanField (default=False)
  - delete_reason: TextField (blank=True, null=True)
  - deleted_at: DateTimeField (blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the purchase
  - purchase_items: returns all purchase items related to this purchase
  - parse_raw_data: parses the raw data and extracts information

Your output should be a valid JSON object. Please strictly adhere to the following output:

{
    "SQLquery": [
        {
            "SQL": "<sql query generated>",
            "reason":"<explanation of the query>",
        }
    ]
}    




    """
    prompt = """
    {query} {docs} {userid}

    """
    def __init__(self, model=None):
        self.transform = Transformer(self.sys_msg, model=model)

    def __call__(self, query: str, docs: str, userid: int) -> str:
        return self.transform(self.prompt.format(query=query, docs=docs, userid=userid))
    

class SQLengine:
    sys_msg = """

Generate a sql query to be performed on postgrsql database. Give in django shell. I'll provide you relevant schema.\
Schema:
i have a purchase table.
i also have tables like brand, category, vendor. but purchase is the most important table. \
Generate SQL queries keeping in mind the schema of purchase table as well as the 3 documents given to you.
DO NOT CHANGE THE NAME OF ANY TABLE.

Brand:
- Fields:
  - name: CharField (max_length=255, unique=True)
  - logo: ImageField (upload_to="brand_logos/", blank=True, null=True)
  - parent_company: CharField (max_length=255, blank=True, null=True)
  - website: URLField (blank=True, null=True)
  - description: TextField (blank=True, null=True)
  - phone: CharField (max_length=255, blank=True, null=True)
  - email: EmailField (blank=True, null=True)
  - address: TextField (max_length=255, blank=True, null=True)
  - city: CharField (max_length=255, blank=True, null=True)
  - country: CharField (max_length=255, blank=True, null=True)
  - tax_id: CharField (max_length=255, blank=True, null=True)
  - tax_id_type: CharField (max_length=255, blank=True, null=True)
  - tax_id_country: CharField (max_length=255, blank=True, null=True)
  - tax_id_state: CharField (max_length=255, blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the brand

Item:
- Fields:
  - brand: ForeignKey to Brand (on_delete=models.CASCADE, null=True, blank=True)
  - name: CharField (max_length=255, unique=True)
  - sku_code: CharField (max_length=255, null=True, blank=True)
  - description: TextField (null=True, blank=True)
  - category: CharField (max_length=255, null=True, blank=True)
- Properties:
  - brand_name: returns the name of the brand associated with the item
- Methods:
  - __str__: returns a string representation of the item

Vendor:
- Fields:
  - name: CharField (max_length=255)
  - logo: ImageField (upload_to="vendor_logos/", blank=True, null=True)
  - website: URLField (blank=True, null=True)
  - description: TextField (blank=True, null=True)
  - phone: CharField (max_length=255, blank=True, null=True)
  - email: EmailField (blank=True, null=True)
  - address: TextField (max_length=255, blank=True, null=True)
  - city: CharField (max_length=255, blank=True, null=True)
  - country: CharField (max_length=255, blank=True, null=True)
  - tax_id: CharField (max_length=255, blank=True, null=True)
  - tax_id_type: CharField (max_length=255, blank=True, null=True)
  - tax_id_country: CharField (max_length=255, blank=True, null=True)
  - tax_id_state: CharField (max_length=255, blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the vendor

Category:
- Fields:
  - name: CharField (max_length=255, unique=True)
- Methods:
  - __str__: returns a string representation of the category

PurchaseItem:
- Fields:
  - item: ForeignKey to Item (on_delete=models.CASCADE)
  - purchase: ForeignKey to Purchase (on_delete=models.CASCADE)
  - quantity: FloatField (blank=True, null=True)
  - unit_price: FloatField (blank=True, null=True)  # in cents
  - total_price: FloatField (blank=True, null=True)  # in cents
  - is_favorite: BooleanField (default=False)
  - seller_name: CharField (max_length=255, blank=True, null=True)
  - seller_address: TextField (max_length=255, blank=True, null=True)
  - seller_email: EmailField (blank=True, null=True)
  - seller_phone: CharField (max_length=255, blank=True, null=True)
  - seller_website: URLField (blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the purchase item

Purchase:
- Fields:
  - transaction_id: CharField (max_length=255)
  - user: ForeignKey to User (on_delete=models.CASCADE)
  - email_image_url: URLField (blank=True, null=True)
  - purchase_image: ImageField (upload_to="purchase_images/", blank=True, null=True)
  - payee_name: CharField (max_length=255, blank=True, null=True)
  - payee_address: TextField (max_length=255, blank=True, null=True)
  - payee_email: EmailField (blank=True, null=True)
  - payee_phone: CharField (max_length=255, blank=True, null=True)
  - vendor: ForeignKey to Vendor (on_delete=models.CASCADE)
  - category: ForeignKey to Category (on_delete=models.CASCADE, null=True, blank=True)
  - payment_method: CharField (max_length=255, blank=True, null=True)
  - last_four_digits: CharField (max_length=4, blank=True, null=True)
  - shipping_amount: FloatField (null=True, blank=True)
  - tax_amount: FloatField (null=True, blank=True)
  - discount_amount: FloatField (null=True, blank=True)
  - total_amount: FloatField
  - date: DateTimeField (default=timezone.now)
  - uploaded_at: DateTimeField (default=timezone.now)
  - is_edited: BooleanField (default=False)
  - edited_at: DateTimeField (blank=True, null=True)
  - note: TextField (blank=True, null=True)
  - source: CharField (max_length=255, choices=SOURCE_CHOICES, default=SOURCE_CHOICES[0][0])
  - raw_data: TextField (blank=True, null=True)
  - html_data: TextField (blank=True, null=True)
  - attachment: ForeignKey to EmailAttachments (on_delete=models.CASCADE, null=True, blank=True)
  - is_deleted: BooleanField (default=False)
  - delete_reason: TextField (blank=True, null=True)
  - deleted_at: DateTimeField (blank=True, null=True)
- Methods:
  - __str__: returns a string representation of the purchase
  - purchase_items: returns all purchase items related to this purchase
  - parse_raw_data: parses the raw data and extracts information

Your output should be a valid JSON object. Please strictly adhere to the following output:

{
    "SQLquery": [
        {
            "SQL": "<sql query generated>",
            "reason":"<explanation of the query>"
        }
    ]
}    




    """
    prompt = """
    {query} {docs}

    """
    def __init__(self, model=None):
        self.transform = Transformer(self.sys_msg, model=model)

    def __call__(self, query: str, docs: str) -> str:
        return self.transform(self.prompt.format(query=query))    

def result(doc1, doc2, query):
        print()
        print('llm getting answer')
        # choice=["list transactions", "don't list transactions"]
        messages = [{
            "role": "user",
            "content": f"Given 2 documents and query, parse the user's documents {doc1} and other user's documents {doc2} and \
            answer the query {query} strictly using the information in {doc2}."\
        }]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "answer_the_query",
                    "description": "Given 2 documents, user query, answer the query STRICTLY using the information in the doc2.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "description": "look at doc1 and understand user's preferences. Then look at doc2 and fetch the answer\
                                for the query from {doc2}. Go through all 3 documents in {doc2}. Don't skip any. \
                                Phrase it in a proper sentence.\
                                Mention the brands and vendors related to the \
                                query compulsarily. Also mandatorily mention the PURCHASE ITEM STRINGS. THis is very very important.\
                                And also add websites relevant to query.\
                                If you don't find anything relevant, say nothing found. Don't return irrelevant transactions"
                            },
                        "transaction_id": {
                            "type": "array",
                            "items": {
                            "type": "number"
                            },
                            "description": "Return a list of transaction IDs for the transactions that you fetched your answers from.\
                            If there are no matching transactions, return empty list."
                            },
                        #  "category": {
                        #     "type": "string",
                        #     "description": "You need to return either 'list transactions' or 'do not list transactions'. \
                        #     If the user query is about experiences, recommendations, or insights based on general transactions, \
                        #     the classification should be 'list transactions'. \
                        #     If the user query pertains to general inquiries or recommendations related to transactions, \
                        #     it should be classified as 'list transactions'. \
                        #     This is so that we can list all the relevant transactions for the user. \
                        #     However, if the user query is solely related to their personal transactions like \
                        #     'What brand did I buy the most' or 'what's my favourite item' etc, then return 'do not list transaction'.",
                        #     "enum": choice
                        #     },
                         
                        },
                        
                        "required": ["answer", "transaction_id"]
                    }
                }
            }
        ]

        try:
            response = client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="mixtral-8x7b-32768",
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            raise Exception("OpenAI API error. Please try again later.")

        # Extract the answer from the response
        print(response)
        
        if response.choices[0].message.tool_calls[0].function:
            response_data = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        
            answer = response_data['answer']
            id=response_data['transaction_id']
            
            print()
            print('Answer:', answer)
            print('ID: ', id)

        return None

def result_my(doc1, query):
        print()
        print('llm getting answer')
        messages = [{
            "role": "user",
            "content": f"Given a document and query, parse my documents {doc1} and \
            answer the query {query} strictly using the information in {doc1}."\
        }]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "answer_the_query",
                    "description": "Given a document and user query, answer the query STRICTLY using the information in the doc1.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "description": "{doc1} contains my transactions. Look at doc1 and fetch the answer\
                                for the query from {doc1}. Go through all 3 documents in {doc1}. Don't skip any. \
                                Phrase it in a proper sentence.\
                                Mention the brands and vendors related to the \
                                query compulsarily. Also mandatorily mention the PURCHASE ITEM STRINGS. THis is very very important.\
                                And also add websites relevant to query.\
                                If you don't find anything relevant, say nothing found. Don't return irrelevant transactions"
                            },
                        "transaction_id": {
                            "type": "array",
                            "items": {
                            "type": "number"
                            },
                            "description": "Return a list of transaction IDs for the transactions that you fetched your answers from.\
                            If there are no matching transactions, return empty list."
                            },
                        #  "category": {
                        #     "type": "string",
                        #     "description": "You need to return either 'list transactions' or 'do not list transactions'. \
                        #     If the user query is about experiences, recommendations, or insights based on general transactions, \
                        #     the classification should be 'list transactions'. \
                        #     If the user query pertains to general inquiries or recommendations related to transactions, \
                        #     it should be classified as 'list transactions'. \
                        #     This is so that we can list all the relevant transactions for the user. \
                        #     However, if the user query is solely related to their personal transactions like \
                        #     'What brand did I buy the most' or 'what's my favourite item' etc, then return 'do not list transaction'.",
                        #     "enum": choice
                        #     },
                         
                        },
                        
                        "required": ["answer", "transaction_id"]
                    }
                }
            }
        ]

        try:
            response = client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="mixtral-8x7b-32768",
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            raise Exception("OpenAI API error. Please try again later.")

        # Extract the answer from the response
        print(response)
        
        if response.choices[0].message.tool_calls[0].function:
            response_data = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            # category=response_data['category']
            answer = response_data['answer']
            id=response_data['transaction_id']
            
            print()
            # print('Category: ', category)
            print('Answer:', answer)
            print('ID: ', id)

        return None  
        
def result_myandother(doc1, doc2, query):
        print()
        print('llm getting answer')
        messages = [{
            "role": "user",
            "content": f"Given 2 documents and query, parse my documents {doc1} and other user's documents {doc2} and \
            answer the query {query} strictly using the information in both {doc1} and {doc2}."\
        }]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "answer_the_query",
                    "description": "Given 2 documents, user query, answer the query STRICTLY using the information in doc1 and doc2.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "description": "Doc1 contains all of my transactions and doc2 contains all of other user's \
                                transactions. Analyse both the documents and fetch the answer\
                                . Go through all 3 documents in {doc1} and {doc2}. Don't skip any. \
                                Phrase it in a proper sentence.\
                                Mention the brands and vendors related to the \
                                query compulsarily. Also mandatorily mention the PURCHASE ITEM STRINGS. THis is very very important.\
                                And also add websites relevant to query.\
                                If you don't find anything relevant, say nothing found. Don't return irrelevant transactions"
                            },
                        "transaction_id": {
                            "type": "array",
                            "items": {
                            "type": "number"
                            },
                            "description": "Return a list of transaction IDs for the transactions that you fetched your answers from.\
                            If there are no matching transactions, return empty list."
                            },
                        #  "category": {
                        #     "type": "string",
                        #     "description": "You need to return either 'list transactions' or 'do not list transactions'. \
                        #     If the user query is about experiences, recommendations, or insights based on general transactions, \
                        #     the classification should be 'list transactions'. \
                        #     If the user query pertains to general inquiries or recommendations related to transactions, \
                        #     it should be classified as 'list transactions'. \
                        #     This is so that we can list all the relevant transactions for the user. \
                        #     However, if the user query is solely related to their personal transactions like \
                        #     'What brand did I buy the most' or 'what's my favourite item' etc, then return 'do not list transaction'.",
                        #     "enum": choice
                        #     },
                         
                        },
                        
                        "required": ["answer", "transaction_id"]
                    }
                }
            }
        ]

        try:
            response = client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="mixtral-8x7b-32768",
                messages=messages,
                tools=tools,
            )
        except Exception as e:
            raise Exception("OpenAI API error. Please try again later.")

        # Extract the answer from the response
        print(response)
        
        if response.choices[0].message.tool_calls[0].function:
            response_data = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            # category=response_data['category']
            answer = response_data['answer']
            id=response_data['transaction_id']
            
            print()
            # print('Category: ', category)
            print('Answer:', answer)
            print('ID: ', id)

        return None                     


                    



def fetch_user_data():
    with open('other_dump.json', 'r') as file:
        user_raw_data = json.load(file)
    documents = [Document(page_content=str(user['purchase_history']), metadata={"userid": user['purchase_history'].get('user_id', '')}) for user in user_raw_data]
    return documents



def search_documents(documents, query, source, userid, category):
        topk=6   
        if category == "my":
            db = FAISS.from_documents(documents, OpenAIEmbeddings(api_key=openai_api_key))
            docs = db.similarity_search_with_score_by_vector(
                OpenAIEmbeddings(api_key=openai_api_key).embed_query(query),
                filter={'userid': userid},
                k=topk
            )
        elif category=="other":
            filtered_docs = [doc for doc in documents if doc.metadata.get('userid') != userid]
            db = FAISS.from_documents(filtered_docs, OpenAIEmbeddings(api_key=openai_api_key))
            docs = db.similarity_search_with_score_by_vector(
                OpenAIEmbeddings(api_key=openai_api_key).embed_query(query),
                documents=filtered_docs,
                k=topk
            )
        else:
            db = FAISS.from_documents(documents, OpenAIEmbeddings(api_key=openai_api_key))
            docs = db.similarity_search_with_score_by_vector(
                OpenAIEmbeddings(api_key=openai_api_key).embed_query(query),
                k=topk
            )
          
    
        for doc, similarity_score in docs:
            inverse_similarity_score = 1 - similarity_score
            print("Document:")
            print(doc.page_content)
            print(f"Similarity Score: {inverse_similarity_score:.4f}")
            print()
        return docs


def process_query(query):
    print('Query:', query)
 
    QC = QueryClassifier()
    response = str(QC(query))  
    response_dict = json.loads(response)
    category = response_dict['category'][0]['classification']
    reason=response_dict['category'][0]['reason']
    print(category)
    print(reason)
    userid=70


    if(category=='My'):
        documents1 = fetch_user_data()
        doc1 = search_documents(documents1, query, "other", userid, "my")
        result_my(doc1, query)
        
    
    elif category=='Other_user':
        documents1 = fetch_user_data()
        print('user data: ')
        doc1 = search_documents(documents1, query, "user", userid, "my")
        print() 
        print()
        print('other user data: ')
        doc2 = search_documents(documents1, query, "other", "otheruser")
        result(doc1, doc2, query)
    
    elif category=='My and Other_user':
        documents1 = fetch_user_data()
        print('user data: ')
        doc1 = search_documents(documents1, query, "other", "my")
        print() 
        print()
        print('other user data: ')
        doc2 = search_documents(documents1, query, "other", "otheruser")
        result_myandother(doc1, doc2, query)
    
    
    
    elif category=='My and SQL':
        print('sql query + docs')
        documents1 = fetch_user_data()
        doc1 = search_documents(documents1, query, "other", 1, "my")
        SE=SQLengineanddocs()
        response=str(SE(query,doc1, 70))
        response_dict = json.loads(response)
        SQLquery = response_dict['SQLquery'][0]['SQL']
        reason=response_dict['SQLquery'][0]['reason']
        print(SQLquery)
        print()
        print(reason)
        print()
        
        
        
    
    elif category=='SQL':
        print('sql query will be performed')
        SE=SQLengine()
        response=str(SE(query))
        print(response)
        
    
    else:
        print('no matching category found') 
    

   

    

if __name__ == "__main__":

    query1='Which was the brand that was most purchased in 2020?'
    query2='Which laptop or desktop is best for intensive gaming and streaming?'
    query3='Which was my most purchased brand in 2020?'
    query4='what tshirts should one carry for a ski trip?'
    query5="What are the best hiking boots for women?"
    query6="What's the best brand for durable backpacks?"
    query7="What's my favorite tag on Instagram?"
    query8 = "Which vendor have I purchased from the least?"
    query9 = "What are the most popular fashion trends among users?"
    query10 = "What are some recommended skincare products based on user reviews?"
    query11 = "Which restaurants do people frequently recommend in this area?"
    query12="Which pizza place offers the best value for money in this city?"
    query13="What's the most popular lipstick shade among makeup enthusiasts?"
    query14="Which tiffin box is recommended for keeping food warm during travel?"
    query15="What are the must-have kitchen gadgets for a home chef?"
    query16="What's the best brand for noise-canceling headphones?"
    query17="What are the latest trends in smart home technology?"
    query17="What should I get Param for his birthday?"
    query18="What's the best cologne I can get from Amazon?"
    query19="Best place to buy seafood or fish?"
    query20="Where can i find the best clothes in India?"
    query21="Which brands do Param and I have in common?"
    query22 = "Which public transportation have i used the most?"
    query23 = "Which restaurants do I and others commonly visit?"
    query24 = "What genres of books are popular among others and me?"
    query25 = "Which electronics brands are commonly owned by others?"
    query26 = "What makeup products are commonly used by women?"
    query27 = "What restaurants are preferred by me and others?"
    query28 = "What movie genres are liked by others and me?"
    query29 = "Where can I get really good seafood?"
    query30 = "What's the total amount I've spent on makeup so far, and what have I purchased?"
    query31 = "how many times have I purchased from Urbanic, what items did I buy and how much have I spent on it in total?"
    query32=  "What's the cheapest thing I've purchased from little box india?"
    query33="How many times have I ordered from Zomato and what do I usually buy?"
    query34="How often have I used public transportation and what are they?"
    

    st = time.time()
    process_query(query33)
    et = time.time()
    print('Time:', et - st)
