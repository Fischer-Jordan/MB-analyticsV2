import json
import random
import string
from datetime import datetime, timedelta
import itertools
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
import time
import requests
import json
total_time=0

word2vec_model_path = 'GoogleNews-vectors-negative300.bin'
word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True, limit=100000)

def preprocess(brand, seller, vendor, caption, item):      
    combined_text = f"{brand} {seller} {vendor} {caption} {item}"
    
    # Tokenization
    tokens = word_tokenize(combined_text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    return filtered_tokens


def generate_tags2(brand, seller, vendor, caption, item, user, id, top_n=10, similarity_threshold=0.5):
    print(f"generating for {user}'s post {id}")
    preprocessed_text = preprocess(brand, seller, vendor, caption, item)
    ans=set(preprocessed_text)
    tag_candidates = []
    
    for word in preprocessed_text:
        if word in word2vec_model.key_to_index:
            word_vector = word2vec_model[word]
            similar_words = word2vec_model.similar_by_vector(word_vector, topn=top_n)
            tag_candidates.extend([word for word, _ in similar_words  if _ > similarity_threshold])
    
    unique_tags = list(set(tag_candidates))[:top_n]
    for word in unique_tags:
        ans.add(word.lower())  
    ans2=list(ans)
    return ans2

# Function to generate random tags
# def generate_tags(*args):
#     tags = []
#     for arg in args:
#         tags.extend(arg.split())
#     return tags

# Function to generate random string
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Common brands, sellers, and vendors
common_brands = ["Nike", "Adidas", "Apple", "Samsung", "Sony", "Gucci", "H&M", "Zara", "Toyota", "Honda"]
common_sellers = ["Best Buy", "Target", "Walmart", "Amazon", "Macy's", "IKEA", "Lowe's", "Home Depot", "Costco", "Starbucks"]
common_vendors = ["Apple Store", "Samsung Store", "Nike Store", "Adidas Store", "Sony Store", "Gucci Store", "H&M Store", "Zara Store", "Toyota Dealership", "Honda Dealership"]
additional_tags = ["sport", "food", "travel", "music", "fitness", "technology", "art", "nature", "books", "photography", "health", "beauty", "culture", "movies", "gaming", "home", "cars", "pets", "outdoors", "education"]

# Function to generate posts
def generate_posts(user, post_count):
    posts = []
    for i in range(1, post_count + 1):
        brand = random.choice(common_brands)
        seller = random.choice(common_sellers)
        vendor = random.choice(common_vendors)
        item = generate_random_string(random.randint(5, 10))
        caption = f"Check out this {item} I got from {seller}"
        post = {
            "id": i,
            "tags": list(set([item.lower()] + random.sample(additional_tags, 3))),
            "date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            "brand": brand,
            "seller": seller,
            "vendor": vendor,
            "caption": caption,
            "item": item,
            "tags2": generate_tags2(brand, seller, vendor, caption, item, user, i)
        }
        posts.append(post)
    return posts

# Generating data for 10 users
users_data = []
for i in range(1, 11):
    st=time.time()
    user = {
        "user": f"user{i}",
        "posts": generate_posts(f"user{i}", 50),
        "likes": [],  # Initialize an empty list for likes
        "post_seen": []  # Initialize an empty list for seen posts
    }
    et=time.time()
    total_time+= et-st
    users_data.append(user)

# Populate likes and seen posts for each user with posts from other users
for user in users_data:
    other_users = [u for u in users_data if u != user]  # Get other users
    for _ in range(10):  # Choose 10 random posts from other users for likes and seen posts
        other_user = random.choice(other_users)
        post_id = random.randint(1, 50)  # Assuming each user has 50 posts
        date = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        # Add like
        user["likes"].append({"author": other_user["user"], "post_id": post_id, "date": date})
        # Add seen post
        user["post_seen"].append({"author": other_user["user"], "post_id": post_id, "date": date})

# Writing data to a JSON file
with open('dummy_data.json', 'w') as file:
    json.dump(users_data, file, indent=4)

print("Data saved to dummy_data.json")
print(f"Total time taken to generate tags2: {total_time} seconds")

