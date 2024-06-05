import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import os
import re

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
]


def post_process_predictions(email, prediction, emoji_count):
    email_lower = email.lower()
    matching_keywords = [
        keyword
        for keyword in invoice_indicative_keywords
        if keyword.lower() in email_lower
    ]
    print(matching_keywords)
    keyword_count = len(matching_keywords)
    print(keyword_count)
    print(emoji_count)
    if keyword_count > 4 and prediction != "invoice":
        return "invoice"
    if emoji_count > 2 and prediction in ["ham", "invoice"]:
        return "spam"
    if keyword_count<2 and prediction == "invoice":
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
    svm_model_path = 'svm_model_1.joblib'
    tfidf_vectorizer_path = 'tfidf_vectorizer_1.joblib'
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
    final_prediction = post_process_predictions(new_email, prediction[0], emoji_count)

    # unload models
    del loaded_svm_model
    del loaded_tfidf_vectorizer

    return final_prediction



def remove_newlines_and_quotes(body):
    body = re.sub(r"[\n\r\t\u200c]", "", body)
    body = re.sub(r"\s+", " ", body)
    body = re.sub(r"[\n\r\"]", "", body)
    body = re.sub(r'\n\s*\n', '\n', body.strip())
    return body


e1="""
HDFC BANKDear Customer, Rs.120.00 has been debited from account **8865 to VPA sk8951429@okicici on 29-04-24. Your UPI transaction reference number is 412095324049. Please call on 18002586161 to report if this transaction was not authorized by you. Warm Regards, HDFC BankFor more details on Service charges and Fees, click here.© HDFC Bank  """
e1=remove_newlines_and_quotes(e1)
print('PROCESSED EMAIL: ', e1)
print('done')
prediction = classify_email(e1)
print(f"The new email is classified as:", prediction)
