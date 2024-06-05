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




def preprocess(brand, seller, vendor, caption, item):   
    print('preprocessing')    
    combined_text = f"{brand} {seller} {vendor} {caption} {item}"
    
    # Tokenization
    tokens = word_tokenize(combined_text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    return filtered_tokens


def generate_tags(brand, seller, vendor, caption, item, top_n=10, similarity_threshold=0.5):
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



def jaccard_similarity(set1, set2, user, author, postid, status):
  def preprocess_set(words):
        processed_set = set()
        for word in words:
            #finding synonyms of the word using wordnet
            synonyms = set()    
            for syn in wordnet.synsets(word, pos=wordnet.NOUN):
                for lemma in syn.lemmas():
                    synonyms.add(lemma.name().lower())
            processed_set.update(synonyms)
        return processed_set

  processed_set1 = preprocess_set(set1)
  processed_set1.update(set1)
  processed_set2 = preprocess_set(set2)
  processed_set2.update(set2)


  intersection = len(processed_set1.intersection(processed_set2))
  union = len(processed_set1.union(processed_set2))
  return intersection / union if union != 0 else 0


def ranking_posts(data):
  for user_data in data:
      user = user_data["user"]
      user_posts = user_data["posts"]
      user_likes = user_data["likes"]
      user_seen = user_data["post_seen"]
      
      combined_tags = []
      for post in user_posts:
          combined_tags.extend(post["tags"])
          combined_tags.extend(post["tags2"])

      
      user_tags = set(combined_tags)
      liked_posts_tags = set()
      for like in user_likes:
        for post_data in data:
              if post_data["user"] == like["author"]:
                for post in post_data["posts"]:
                    if post["id"]==like["post_id"]:
                      liked_posts_tags.update(post["tags"])
                      liked_posts_tags.update(post["tags2"])
                break
              
      
      posts_with_similarity = []
      for post_data in data:
          if post_data["user"] == user:
              continue 
            
          
          for post in post_data["posts"]:
              post_tags = set(post["tags"] + post["tags2"])
              
                
              unseen_jaccard_index = jaccard_similarity(post_tags, user_tags.union(liked_posts_tags), user, post_data["user"], post["id"], "unseen")
              seen_jaccard_index = jaccard_similarity(post_tags, user_tags,user, post_data["user"], post["id"],"seen")
              
              
              unseen = True
              liked=False
              for seen_post in user_seen:
                  if seen_post["author"] == post_data["user"] and seen_post["post_id"] == post["id"]:
                      unseen = False
                      break
              
              for like in user_likes:
                  if like["author"] == post_data["user"] and like["post_id"] == post["id"]:
                      liked = True
                      break
              
              posts_with_similarity.append({
                  "id": post["id"],
                  "author": post_data["user"],
                  "tags": post["tags"],
                  "tags2": post["tags2"],
                  "unseen_jaccard_index": unseen_jaccard_index if unseen else None,
                  "seen_jaccard_index": seen_jaccard_index if liked else None,
                  "unseen": unseen,
                  "liked": liked
              })
      
      # Sort posts based on Jaccard index (highest to lowest similarity) and unseen-ness
      sorted_posts = sorted(posts_with_similarity, key=lambda x: (not x["unseen"], -x["unseen_jaccard_index"] if x["unseen_jaccard_index"] is not None else 0, -x["seen_jaccard_index"] if x["seen_jaccard_index"] is not None else 0))
      
      print(f"{user}:")
      for post in sorted_posts:
          print(f"Post {post['id']} of {post['author']} - Jaccard Index: {post['seen_jaccard_index'] if post['seen_jaccard_index'] is not None else post['unseen_jaccard_index']}, {'Unseen' if post['unseen'] else 'Seen'}")


      # Add user's own posts
      for post in user_posts:
          print(f"Post {post['id']} of {user}")
      print()
      
      
def draw_graph(data):
  G = nx.DiGraph()

  # Add users as nodes
  for i, user_data in enumerate(data):
      G.add_node(user_data["user"], size=4000, color="green", pos=(i, 0))

  # Add posts as nodes and edges for likes and views
  for user_data in data:
      user = user_data["user"]
      for post in user_data["posts"]:
          post_id = post["id"]
          post_name = f"{user}'s post {post_id}"
          G.add_node(post_name, size=1000, color="blue", pos=(0, 0))
          G.add_edge(user, post_name, type="")
          for like in user_data["likes"]:
              liked_post_author = like["author"]
              liked_post_id = like["post_id"]
              G.add_edge(user, f"{liked_post_author}'s post {liked_post_id}", type="liked, seen")

          for seen_post in user_data["post_seen"]:
              seen_post_author = seen_post["author"]
              seen_post_id = seen_post["post_id"]
              # Check if the post is not liked
              if not any(like["post_id"] == seen_post_id for like in user_data["likes"]):
                  G.add_edge(user, f"{seen_post_author}'s post {seen_post_id}", type="seen")


  # Draw the graph
  pos = nx.spring_layout(G, k=0.3, iterations=50)  # Adjust k and iterations for better layout
  pos = {node: (x - 0.5, y) for node, (x, y) in pos.items()}
  # Manually set the x-coordinates of user nodes to provide equal gaps
  user_nodes = [node for node in G.nodes if isinstance(node, str)]
  x_coordinates = range(len(user_nodes))
  for user, x in zip(user_nodes, x_coordinates):
      pos[user] = (x, 1.5)

  # Position user's posts close to the respective user nodes
  post_y_offset = -0.2
  for user_data in data:
      user = user_data["user"]
      user_posts = [f"{user}'s post {post['id']}" for post in user_data["posts"]]
      for post_name in user_posts:
          pos[post_name] = (pos[user][0], pos[user][1] + post_y_offset)
          post_y_offset -= 0.1  # Adjust the distance between user posts

  # Draw the graph nodes
  node_sizes = [G.nodes[node]["size"] if "size" in G.nodes[node] else 1000 for node in G.nodes]
  node_colors = [G.nodes[node]["color"] if "color" in G.nodes[node] else "blue" for node in G.nodes]
  nx.draw(
      G,
      pos,
      with_labels=True,
      node_size=node_sizes,
      node_color=node_colors,
      font_size=10,
      font_weight="bold",
      arrows=True,
  )

  # Draw the post node labels with tags
  for node_name in G.nodes:
      if "post" in node_name:
          tags = " ".join([tag for post_data in data for post in post_data["posts"] if f"{post_data['user']}'s post {post['id']}" == node_name for tag in post["tags"]])
          plt.text(pos[node_name][0] + 0.12, pos[node_name][1] -0.02,  f"{tags}", fontsize=8, ha='left')
          tags2 = " ".join([tag for post_data in data for post in post_data["posts"] if f"{post_data['user']}'s post {post['id']}" == node_name for tag in post["tags2"]])
          plt.text(pos[node_name][0] + 0.12, pos[node_name][1] -0.05,  f"{tags2}", fontsize=8, ha='left')

  # Draw the edge labels
  edge_labels = {(u, v): d["type"] for u, v, d in G.edges(data=True)}
  nx.draw_networkx_edge_labels(
      G,
      pos,
      edge_labels=edge_labels,
      font_color='red',  # You can customize font color here
  )

  plt.show()


    
if __name__ == "__main__":
  print('start')
  st=time.time()
  word2vec_model_path = 'GoogleNews-vectors-negative300.bin'
  word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True, limit=100000)
  print('loading done')
 #if: 
    
        #   data=[
        #     {
        #         "user": "param",
        #         "posts": [
        #             {
        #                 "id": 1,
        #                 "tags": ["loveit", "yummy", "biryani", "bestbiryani", "biryanilover"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Meghana Biryani",
        #                 "seller": "Meghana Food Court",
        #                 "vendor": "Meghana Caterers",
        #                 "caption": "Indulging in some heavenly biryani! Who can resist?",
        #                 "item":"Chicken Biryani",
        #                 "tags2": generate_tags("Meghana Biryani", "Meghana Food Court", "Meghana Caterers", "Indulging in some heavenly biryani! Who can resist?", "Chicken Biryani")
        #             },
        #             {
        #                 "id": 2,
        #                 "tags": ["nikeshoes", "nike", "justdoit", "sports", "shoes"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Nike",
        #                 "seller": "Nike ",
        #                 "vendor": "Nike Inc.",
        #                 "caption": "Stepping up my game with these sleek kicks! #JustDoIt",
        #                 "item":"Shoes",
        #                 "tags2": generate_tags("Nike", "Nike ", "Nike Inc.", "Stepping up my game with these sleek kicks! #JustDoIt", "Shoes")
        #             },
        #             {
        #                 "id": 3,
        #                 "tags": ["iphone", "apple", "anappleaday", "iphone15", "iphonelover"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Apple",
        #                 "seller": "Apple ",
        #                 "vendor": "Apple Inc.",
        #                 "caption": "Caught in the Apple ecosystem! Can't get enough.",
        #                 "item":"iphone",
        #                 "tags2": generate_tags("Apple", "Apple ", "Apple Inc.", "Caught in the Apple ecosystem! Cannot get enough.", "iphone")
        #             },
        #             {
        #                 "id": 4,
        #                 "tags": ["lays", "bluelays", "junkfood", "lovejunk"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Lays",
        #                 "seller": "More Supermarket",
        #                 "vendor": "More Supermarket",
        #                 "caption": "Crunching away on some classic Lay's chips! #SnackTime",
        #                 "item":"chips",
        #                 "tags2": generate_tags("Lays", "More Supermarket", "More Supermarket", "Crunching away on some classic Lay's chips! #SnackTime", "chips")
        #             },
        #             {
        #                 "id": 5,
        #                 "tags": ["uber", "safetrip", "5stars", "drive", "cheapdrive"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Uber",
        #                 "seller": "Uber Technologies Inc.",
        #                 "vendor": "Uber",
        #                 "caption": "Getting around town with Uber! Safe, reliable, and convenient.",
        #                 "item":"Marathalli Metro station",
        #                 "tags2": generate_tags("Uber", "Uber Technologies Inc.", "Uber", "Getting around town with Uber! Safe, reliable, and convenient.", "Marathahalli metro station")
        #             }
        #         ],
        #         "likes": [
        #             {
        #                 "author": "khushi",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "om",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "om",
        #                 "post_id": 3,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ],
        #         "post_seen": [
        #             {
        #                 "author": "khushi",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "om",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "om",
        #                 "post_id": 3,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ]
        #     },
        #     {
        #         "user": "swathi",
        #         "posts": [
        #             {
        #                 "id": 1,
        #                 "tags": ["biryani", "lovebiryani", "yummy", "loveit"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Hyderabadi Delights",
        #                 "seller": "Hyderabadi Delights Restaurant",
        #                 "vendor": "Hyderabadi Delights ",
        #                 "caption": "Savoring the rich flavors of Hyderabadi biryani! A true delight.",
        #                 "item":"Veg Biryani",
        #                 "tags2": generate_tags("Hyderabadi Delights", "Hyderabadi Delights Restaurant", "Hyderabadi Delights ", "Savoring the rich flavors of Hyderabadi biryani! A true delight.", "veg biryani")
        #             },
        #             {
        #                 "id": 2,
        #                 "tags": ["newwaterbottle", "tupperware", "lovetupperware"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Tupperware",
        #                 "seller": "Tupperware",
        #                 "vendor": "Tupperware",
        #                 "caption": "Stay hydrated with Tupperware's durable water bottles! #StayHydrated",
        #                 "item":"Water Bottle",
        #                 "tags2": generate_tags("Tupperware", "Tupperware", "Tupperware", "Stay hydrated with Tupperware's durable water bottles! #StayHydrated", "water bottle")
        #             },
        #             {
        #                 "id": 3,
        #                 "tags": ["floweringplant", "flowers", "pretty", "rose", "redrose", "plant"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Blooms & Petals",
        #                 "seller": "Blooms & Petals Nursery",
        #                 "vendor": "Blooms & Petals ",
        #                 "caption": "Adding a touch of nature to my home with these beautiful flowering plants! #NatureLover",
        #                 "item":"Rose plant",
        #                 "tags2": generate_tags("Blooms & Petals", "Blooms & Petals Nursery", "Blooms & Petals ", "Adding a touch of nature to my home with these beautiful flowering plants! #NatureLover", "rose plant")
        #             }
        #         ],
        #         "likes": [
        #             {
        #                 "author": "khushi",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "param",
        #                 "post_id": 3,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ],
        #         "post_seen": [
        #             {
        #                 "author": "khushi",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "om",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "param",
        #                 "post_id": 3,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ]
        #     },
        #     {
        #         "user": "om",
        #         "posts": [
        #             {
        #                 "id": 1,
        #                 "tags": ["iphone15", "apple", "newiphone", "applelove", "iphone"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Apple",
        #                 "seller": "Apple",
        #                 "vendor": "Apple Inc.",
        #                 "caption": "Exploring the latest iPhone features! Apple never disappoints.",
        #                 "item":"iphone 15",
        #                 "tags2": generate_tags("Apple", "Apple", "Apple Inc.", "Exploring the latest iPhone features! Apple never disappoints.", "iphone 15")
        #             },
        #             {
        #                 "id": 2,
        #                 "tags": ["macbook", "mac", "apple"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Apple",
        #                 "seller": "Apple ",
        #                 "vendor": "Apple Inc.",
        #                 "caption": "Boosting productivity with the power of MacBooks! #AppleLove",
        #                 "item":"Laptop",
        #                 "tags2": generate_tags("Apple", "Apple ", "Apple Inc.", "Boosting productivity with the power of MacBooks! #AppleLove", "laptop")
        #             },
        #             {
        #                 "id": 3,
        #                 "tags": ["flower", "rose", "marigold", "garden", "plant"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Garden Glory",
        #                 "seller": "Garden Glory Nursery",
        #                 "vendor": "Garden Glory ",
        #                 "caption": "Adding a splash of color to my garden with these vibrant flowers! #GardenDecor",
        #                 "item":"Marigold plant",
        #                 "tags2": generate_tags("Garden Glory", "Garden Glory Nursery", "Garden Glory ", "Adding a splash of color to my garden with these vibrant flowers! #GardenDecor", "marigold plant")
        #             }
        #         ],
        #         "likes": [
        #             {
        #                 "author": "swathi",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "param",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ],
        #         "post_seen": [
        #             {
        #                 "author": "swathi",
        #                 "post_id": 2,
        #                 "date": "2024-02-22T10:00:00"
        #             },
        #             {
        #                 "author": "param",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ]
        #     },
        #     {
        #         "user": "khushi",
        #         "posts": [
        #             {
        #                 "id": 1,
        #                 "tags": ["tupperware", "cooking", "newcook", "utensils"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Tupperware",
        #                 "seller": "Tupperware",
        #                 "vendor": "Tupperware",
        #                 "caption": "Cooking up a storm with Tupperware's kitchen essentials! #CookingTime",
        #                 "item":"Bowl",
        #                 "tags2": generate_tags("Tupperware", "Tupperware", "Tupperware", "Cooking up a storm with Tupperware's kitchen essentials! #CookingTime", "bowl")
        #             },
        #             {
        #                 "id": 2,
        #                 "tags": ["kurkure", "lays", "junkfood", "junk"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Kurkure",
        #                 "seller": "Pai s",
        #                 "vendor": "Pai s",
        #                 "caption": "Snacking on some crunchy Kurkure! #SnackAttack",
        #                 "item":"chips",
        #                 "tags2": generate_tags("Kurkure", "Pai s", "Pai s", "Snacking on some crunchy Kurkure! #SnackAttack", "chips")
        #             },
        #             {
        #                 "id": 3,
        #                 "tags": ["shoes", "bata", "loveshoes", "sports"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Bata",
        #                 "seller": "Bata",
        #                 "vendor": "Bata India Limited",
        #                 "caption": "Stepping out in style with Bata shoes! #ShoeLove",
        #                 "item":"Fancy Shoes ",
        #                 "tags2": generate_tags("Bata", "Bata", "Bata India Limited", "Stepping out in style with Bata shoes! #ShoeLove","fancy shoes")
        #             },
        #             {
        #                 "id": 4,
        #                 "tags": ["lenskart", "glasses", "lovethem", "eyes"],
        #                 "date": "2024-02-22T10:00:00",
        #                 "brand": "Lenskart",
        #                 "seller": "Lenskart",
        #                 "vendor": "Lenskart  ",
        #                 "caption": "Accessorizing with trendy glasses from Lenskart! #EyewearFashion",
        #                 "item":"Spectacles",
        #                 "tags2": generate_tags("Lenskart", "Lenskart", "Lenskart  ", "Accessorizing with trendy glasses from Lenskart! #EyewearFashion", "spectacles")
        #             }
        #         ],
        #         "likes": [
        #             {
        #                 "author": "swathi",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ],
        #         "post_seen": [
        #             {
        #                 "author": "swathi",
        #                 "post_id": 1,
        #                 "date": "2024-02-22T10:00:00"
        #             }
        #         ]
        #     }
        # ]
  with open('dummy_data.json', 'r') as file:
        data = json.load(file)
  ranking_posts(data)
  et=time.time()
  print("TOTAL TIME: ", et-st)
  
  draw_graph(data)
