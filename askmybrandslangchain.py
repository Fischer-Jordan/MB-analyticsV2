from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
import json
from langchain.schema import Document
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)

with open('user_data.json', 'r') as file:
    raw_data = json.load(file)
    

documents=[]
for user in raw_data:
    purchase_history = user['purchase_history']
    document = Document(page_content=str(purchase_history))
    documents.append(document)


# Embed the documents and load them into the vector store
db = Chroma.from_documents(documents, OpenAIEmbeddings(api_key=api_key))


# Embed the user's query
# embedding_vector = OpenAIEmbeddings(api_key=api_key).embed_query("param asked which brand is good for sports")
# embedding_vector = OpenAIEmbeddings(api_key=api_key).embed_query("best restaurants to visit")
# embedding_vector = OpenAIEmbeddings(api_key=api_key).embed_query("recommend some good gaming laptops")

# embedding_vector = OpenAIEmbeddings(api_key=api_key).embed_query("what brands are trending right now?")
embedding_vector = OpenAIEmbeddings(api_key=api_key).embed_query("param asked which brand is best suited for me?")



# Query the vector store
docs = db.similarity_search_by_vector_with_relevance_scores(embedding_vector, k=3)
for doc, similarity_score in docs:
    inverse_similarity_score = 1 - similarity_score    
    print("Document:")
    print(doc.page_content)
    print(f"Similarity Score: {inverse_similarity_score:.4f}")
    print()




