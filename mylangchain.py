import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import json

api_key = "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"
client = OpenAI(api_key=api_key)



# Encode purchase history into vector representation for each user
def encode_purchase_history(user_data):
    vector_db = {}
    for user in user_data:
        username = user["username"]
        purchase_history = user["purchase_history"]
        text_data = ' '.join(purchase_history.values())
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text_data])
        vector_db[username] = {
            "vectorizer": vectorizer,
            "vectors": vectors
        }
    return vector_db

def generate_response(prompt):
    messages = [{
        "role": "user",
        "content": f"Given the vector database and the user's prompt, generate the right answer"
    }]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "answer_questions",
                "description": "Given the vector database, correctly answer user's question {prompt}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string",
                            "description": "Given vector DB and the user's question {prompt}, fetch right answer",
                            
                        }
                    },
                    "required": ["answer"]
                }
            }
        }
    ]
    try: 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
        )
    except Exception as e:
        raise Exception("OpenAI API error. Please try again later.")
    
    # Step 2: check if GPT wanted to call a function
    if response.choices[0].message.tool_calls[0].function:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return None
  
# Given JSON data
user_data = [
    {
        "username": "swathi",
        "purchase_history": {
            "purchased_brands": ["Nike", "Adidas", "Puma"],
            "purchased_vendors": ["Amazon", "Flipkart"],
            "purchased_items": ["Running Shoes", "T-shirts", "Backpack"],
            "purchased_categories": ["Footwear", "Apparel", "Accessories"],
            "mycaptions": ["Great day for a run!", "New kicks, who dis?"],
            "mytags": ["#fitness", "#fashion"],
            "liked_brands": ["Nike", "Adidas"],
            "liked_captions": ["Awesome view!", "Sunset vibes 🌇"],
            "liked_tags": ["#nature", "#photography"]
        }
    },
    {
        "username": "param",
        "purchase_history": {
            "purchased_brands": ["Apple", "Samsung"],
            "purchased_vendors": ["Best Buy", "Apple Store"],
            "purchased_items": ["iPhone", "Smartwatch"],
            "purchased_categories": ["Electronics", "Gadgets"],
            "mycaptions": ["New gadget alert!", "Loving my new phone."],
            "mytags": ["#tech", "#gadgets"],
            "liked_brands": ["Apple"],
            "liked_captions": ["City lights ✨", "Chilling with friends."],
            "liked_tags": ["#cityscape", "#friends"]
        }
    },
    {
        "username": "om",
        "purchase_history": {
            "purchased_brands": ["Sony", "Bose"],
            "purchased_vendors": ["Target", "Sony Store"],
            "purchased_items": ["Headphones", "Speakers"],
            "purchased_categories": ["Electronics", "Audio"],
            "mycaptions": ["Music vibes 🎶", "Enjoying the beats."],
            "mytags": ["#music", "#audio"],
            "liked_brands": ["Bose"],
            "liked_captions": ["Beach day!", "Summer vibes ☀️"],
            "liked_tags": ["#beach", "#summer"]
        }
    }
]
user_query = "What brand am I most likely to buy?"


def retrieve_context(user_query, vector_db):
    query_vectorizer = TfidfVectorizer()
    query_vector = query_vectorizer.fit_transform([user_query])
    similarities = {}
    for username, data in vector_db.items():
        similarity = cosine_similarity(query_vector, data["vectors"])
        similarities[username] = similarity[0][0]
    most_similar_user = max(similarities, key=similarities.get)
    return most_similar_user, vector_db[most_similar_user]
  
vector_db = encode_purchase_history(user_data)

# Retrieve relevant context from vector DB based on user's query
user, context = retrieve_context(user_query, vector_db)
print('CONTEXT: ', context)

response = generate_response(context)
print("Response:", response)