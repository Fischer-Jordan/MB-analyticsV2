from gensim.models import KeyedVectors
from nltk.corpus import wordnet
import nltk
# nltk.download('wordnet')


import time

def jaccard_similarity_old(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def jaccard_similarity(set1, set2, word2vec_model):
    def preprocess_set(words):
        processed_set = set()
        for word in words:
            #finding similar words using word2vec
            processed_set.add(word)
            if word in word2vec_model:
                similar_words = [similar_word for similar_word, _ in word2vec_model.similar_by_word(word)]
                processed_set.update(similar_words)
            
            #finding synonyms of the word using wordnet
            synonyms = set()    
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonyms.add(lemma.name().lower())
            processed_set.update(synonyms)
        return processed_set

    processed_set1 = preprocess_set(set1)
    processed_set2 = preprocess_set(set2)
    print()
    print("ORIGINAL: ", set1)
    print("SET 1: ", processed_set1)
    print()
    print("ORIGINAL: ", set2)
    print("SET 2: ", processed_set2)
    print()


    intersection = len(processed_set1.intersection(processed_set2))
    union = len(processed_set1.union(processed_set2))
    return intersection / union if union != 0 else 0



if __name__ == "__main__":
    st=time.time()
    
    set1={'rose','rosebud','rosy', 'flower'}
    set2={'rose', 'flowering'}
    
    set3={'lillies','tulips','marigold'}
    set4={'daffodils', 'sunflower', 'nursery', 'garden'}
    
    set5={'tupperware', 'spoons', 'plates', 'utensils', 'plastic'}
    
    word2vec_model_path = 'GoogleNews-vectors-negative300.bin'
    word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True, limit=100000)
    print("SIMPLE JACCARD: ", jaccard_similarity_old(set1,set2))
    print("COMPLEX JACCARD: ", jaccard_similarity(set1,set2, word2vec_model))
    
    print('-------------------------------------------------------------------')
    print()
    print("SIMPLE JACCARD: ", jaccard_similarity_old(set3,set4))
    print("COMPLEX JACCARD: ", jaccard_similarity(set3,set4, word2vec_model))
    
    
    print('-------------------------------------------------------------------')
    print()
    print("SIMPLE JACCARD: ", jaccard_similarity_old(set4,set5))
    print("COMPLEX JACCARD: ", jaccard_similarity(set4,set5, word2vec_model))
    et=time.time()
    print()
    print("TIME: ", et-st)
