import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import os


def count_emojis(text):
    return emoji.emoji_count(text)


invoice_indicative_keywords = [
    "invoice #",
    "order number",
    "order #",
    "invoice",
    "purchase",
    "hsn code",
    "bill to",
    "total invoice value",
    "ship to",
    "address",
    "tax invoice",
    "order id",
    "receipt",
    "billing",
    "payment",
    "transaction",
    "due date",
    "amount due",
    "credit",
    "debit",
    "account statement",
    "balance",
    "invoice date",
    "payment due",
    "total amount",
    "payable",
    "purchase order",
    "confirmation",
    "shipping",
    "tracking",
    "shipment",
    "dispatch",
    "delivery",
    "order confirmation",
    "receipt number",
    "payment details",
    "invoice total",
    "itemized bill",
    "order"
]


def post_process_predictions(email, prediction, emoji_count):
    email_lower = email.lower()
    matching_keywords = [
        keyword
        for keyword in invoice_indicative_keywords
        if keyword.lower() in email_lower
    ]
    keyword_count = len(matching_keywords)
    if keyword_count > 4 and prediction != "invoice":
        return "invoice"
    if emoji_count > 2 and prediction in ["ham", "invoice"]:
        return "spam"
    return prediction


# Preprocessing function
def preprocess(text):
    text = str(text).lower().replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    text = " ".join(
        [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    )
    return text


# classifying a new email
def classify_email(new_email):
    # Load the pre-trained model and vectorizer
    svm_model_path =  "svm_model_subject.joblib"
    tfidf_vectorizer_path = "tfidf_vectorizer_subject.joblib"
    
    loaded_svm_model = joblib.load(svm_model_path)
    loaded_tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)

    preprocessed_email = preprocess(new_email)
    tfidf_features = loaded_tfidf_vectorizer.transform([preprocessed_email])
    exclamation_mark_count = preprocessed_email.count("!")
    has_invoice_keyword = any(
        keyword in preprocessed_email.lower() for keyword in invoice_indicative_keywords
    )
    numeric_count = sum(c.isdigit() for c in preprocessed_email)
    percentage_sign_count = preprocessed_email.count("%")
    dollar_symbol_count = preprocessed_email.count("$")
    rupee_symbol_count = preprocessed_email.count("₹")
    emoji_count = count_emojis(preprocessed_email)

    # Create a feature vector
    feature_vector = tfidf_features.toarray()[0].tolist()
    feature_vector.extend(
        [
            exclamation_mark_count,
            int(has_invoice_keyword),
            numeric_count,
            percentage_sign_count,
            dollar_symbol_count,
            rupee_symbol_count,
            emoji_count,
        ]
    )

    # Make a prediction using the loaded SVM model
    prediction = loaded_svm_model.predict([feature_vector])
    confidence_scores = loaded_svm_model.predict_proba([feature_vector])
    confidence_invoice = confidence_scores[0][0]
    confidence_spam=confidence_scores[0][1]
    print('prediction: ', prediction)
    print(f"confidence %invoice:  {confidence_invoice*100} ")
    print(f"confidence %spam:  {confidence_spam*100}")
    
    final_prediction = post_process_predictions(new_email, prediction[0], emoji_count)

    # unload models
    del loaded_svm_model
    del loaded_tfidf_vectorizer

    return final_prediction




# if:
    # import emoji
    # from nltk.corpus import stopwords
    # from nltk.stem import WordNetLemmatizer
    # import joblib
    # import os


    # def count_emojis(text):
    #     return emoji.emoji_count(text)


    # invoice_indicative_keywords = [
    #     "invoice #",
    #     "order number",
    #     "order #",
    #     "invoice",
    #     "purchase",
    #     "hsn code",
    #     "bill to",
    #     "total invoice value",
    #     "ship to",
    #     "address",
    #     "tax invoice",
    #     "order id",
    #     "receipt",
    #     "billing",
    #     "payment",
    #     "transaction",
    #     "due date",
    #     "amount due",
    #     "credit",
    #     "debit",
    #     "account statement",
    #     "balance",
    #     "invoice date",
    #     "payment due",
    #     "total amount",
    #     "payable",
    #     "purchase order",
    #     "confirmation",
    #     "shipping",
    #     "tracking",
    #     "shipment",
    #     "dispatch",
    #     "delivery",
    #     "order confirmation",
    #     "receipt number",
    #     "payment details",
    #     "invoice total",
    #     "itemized bill",
    # ]


    # def post_process_predictions(email, prediction, emoji_count):
    #     email_lower = email.lower()
    #     matching_keywords = [
    #         keyword
    #         for keyword in invoice_indicative_keywords
    #         if keyword.lower() in email_lower
    #     ]
    #     keyword_count = len(matching_keywords)
    #     if keyword_count > 10 and prediction != "invoice":
    #         return "invoice"
    #     if emoji_count > 5 and prediction in ["ham", "invoice"]:
    #         return "spam"
    #     return prediction


    # # Preprocessing function
    # def preprocess(text):
    #     text = str(text).lower().replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    #     stop_words = set(stopwords.words("english"))
    #     lemmatizer = WordNetLemmatizer()
    #     text = " ".join(
    #         [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    #     )
    #     return text


    # # classifying a new email
    # def classify_email(new_subject, new_text):
    #     # Load the pre-trained model and vectorizer
    #     svm_model_path =  "svm_model_combined.joblib"
    #     tfidf_vectorizer_text_path = "tfidf_vectorizer_text.joblib"
    #     tfidf_vectorizer_subject_path = "tfidf_vectorizer_subject.joblib"
        
    #     loaded_svm_model = joblib.load(svm_model_path)
    #     loaded_tfidf_vectorizer_text = joblib.load(tfidf_vectorizer_text_path)
    #     loaded_tfidf_vectorizer_subject = joblib.load(tfidf_vectorizer_subject_path)

    #     preprocessed_subject = preprocess(new_subject)
    #     preprocessed_text = preprocess(new_text)
        
    #     tfidf_features_subject = loaded_tfidf_vectorizer_subject.transform([preprocessed_subject])
    #     tfidf_features_text = loaded_tfidf_vectorizer_text.transform([preprocessed_text])
        
    #     exclamation_mark_count = preprocessed_text.count("!")
    #     has_invoice_keyword = any(
    #         keyword in preprocessed_text.lower() for keyword in invoice_indicative_keywords
    #     )
    #     numeric_count = sum(c.isdigit() for c in preprocessed_text)
    #     percentage_sign_count = preprocessed_text.count("%")
    #     dollar_symbol_count = preprocessed_text.count("$")
    #     rupee_symbol_count = preprocessed_text.count("₹")
    #     emoji_count = count_emojis(preprocessed_text)

    #     # Create a feature vector
    #     feature_vector_text = tfidf_features_text.toarray()[0].tolist()
    #     feature_vector_text.extend(
    #         [
    #             exclamation_mark_count,
    #             int(has_invoice_keyword),
    #             numeric_count,
    #             percentage_sign_count,
    #             dollar_symbol_count,
    #             rupee_symbol_count,
    #             emoji_count,
    #         ]
    #     )
        
    #     # Concatenate subject and text features
    #     feature_vector_combined = list(tfidf_features_subject.toarray()[0]) + feature_vector_text

    #     # Make a prediction using the loaded SVM model
    #     prediction = loaded_svm_model.predict([feature_vector_combined])
        
    #     final_prediction = post_process_predictions(new_text, prediction[0], emoji_count)

    #     # Unload models
    #     del loaded_svm_model
    #     del loaded_tfidf_vectorizer_text
    #     del loaded_tfidf_vectorizer_subject

    #     return final_prediction


sub1="Mom glows best ✨ FREE radiant gift"
 

sub2="	Erin, Put Some Pep in Your Step and Save 20% ☀️🏖️	"


sub3="""
	Fwd: Welcome to Brain Pattern Mapping with Break Method
"""


sub4="Celebrating One Year of Sam Edelman ReLove"


sub5="Could it be Endo, PCOS, or something else? 🌱"


sub6="Delivered: Your Amazon.com order #112-9739103-5127468"


sub7="Your renewal request is ready to go"


sub8="Your renewal request is ready to go"


sub9="NYU Alumni Summer Series—Night with the Yankees and Dodgers"


sub10="""
Confirmation: We received your home loan payment
"""


print('-------------------------------------------')
print(sub1)
print()
print(classify_email(sub1))
print('-------------------------------------------')
print(sub2)
print()
print(classify_email(sub2))
print('-------------------------------------------')
print(sub3)
print()
print(classify_email(sub3))
print('-------------------------------------------')
print(sub4)
print()
print(classify_email(sub4))
print('-------------------------------------------')
print(sub5)
print()
print(classify_email(sub5))
print('-------------------------------------------')
print(sub6)
print()
print(classify_email(sub6))
print('-------------------------------------------')
print(sub7)
print()
print(classify_email(sub7))
print('-------------------------------------------')
print(sub8)
print()
print(classify_email(sub8))
print('-------------------------------------------')
print(sub9)
print()
print(classify_email(sub9))
print('-------------------------------------------')
print(sub10)
print()
print(classify_email(sub10))


