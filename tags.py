from gensim.models import KeyedVectors
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# nltk.download('stopwords')
import time



word2vec_model_path = 'GoogleNews-vectors-negative300.bin'
word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)


# try:
#     print("Loading Word2Vec model...")
#     st = time.time()
#     word2vec_model = KeyedVectors.load(saved_model_path)
#     et = time.time()
#     loading_time = et - st
#     print("Word2Vec model loaded successfully.")
#     print("Loading time:", loading_time)
    
# except FileNotFoundError:
#     print("Word2Vec model not found. Creating and saving a new one...")
#     st = time.time()
#     word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
#     et = time.time()
#     loading_time = et - st
#     print("Word2Vec model created and loaded successfully.")
#     print("Loading time:", loading_time)
#     print("Saving Word2Vec model for future use...")
#     word2vec_model.save(saved_model_path)

def preprocess(brand, seller, vendor, caption):
    
    print('preprocessing')    
    combined_text = f"{brand} {seller} {vendor} {caption}"
    
    # Tokenization
    tokens = word_tokenize(combined_text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    tokens=set(filtered_tokens)
    return filtered_tokens


def generate_tags(brand, seller, vendor, caption, top_n=5, similarity_threshold=0.8):
    preprocessed_text = preprocess(brand, seller, vendor, caption)
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
    return ans

if __name__ == "__main__":
    st=time.time()
    brand = "Nike"
    seller = "Nike Store"
    vendor = "Nike Inc."
    caption = "Stepping up my game with these sleek kicks! #JustDoIt"
    tags = list(generate_tags(brand, seller, vendor, caption))
    print("Generated Tags:", tags)
    
    
    brand= "Lenskart",
    seller= "Lenskart",
    vendor= "Lenskart Store Pvt. Ltd.",
    caption= "Accessorizing with trendy glasses from Lenskart! #EyewearFashion"   
    tags = list(generate_tags(brand, seller, vendor, caption))
    print("Generated Tags:", tags)
    
    
    et=time.time()
    print('time: ', et-st)
    

