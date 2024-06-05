# import pandas as pd
# import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import time


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
    "Delivered",
    "Total paid",
    "Items ordered",
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
    if keyword_count > 5 and prediction != "invoice":
        return "invoice"
    if keyword_count < 2 and prediction == "invoice":
        return "ham"
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


# Load the pre-trained model and vectorizer
loaded_svm_model = joblib.load("svm_model_1.joblib")
loaded_tfidf_vectorizer = joblib.load("tfidf_vectorizer_1.joblib")


# classifying a new email
def classify_new_email(new_email):
    preprocessed_email = preprocess(new_email)
    tfidf_features = loaded_tfidf_vectorizer.transform([preprocessed_email])
    exclamation_mark_count = preprocessed_email.count("!")
    has_invoice_keyword = any(
        keyword in preprocessed_email.lower()
        for keyword in invoice_indicative_keywords  #
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
    final_prediction = post_process_predictions(
        new_email, prediction[0], emoji_count
    )  #

    return final_prediction


e1 = """
 ECCO | Laid-back luxury with BIOM C-TRAIL Discover \
    shoes and bags to elevate your everyday style ͏\
     Buy now. Pay with Klarna.View in browserMenWomenOutdoorGolfSaleThe \
        Weekend Wardrobe Elevate your everyday dressing by playing with layers \
    and accents. @carolinelossberg wears the limited edition ECCO BIOM C-TRAIL by Natacha Ramsay-Levi, styled with items in matching earthy tones and a chunky chain-embellished ECCO POT BAG for added luxury.ECCO WOMEN'S BIOM C-TRAIL SNEAKER3 Colors$265ECCO CHAIN POT BAG2 Colors$220Shop NowShop NowDiscover SneakersDiscover Bags & AccessoriesFree Shipping Don't forget, your ECCO account comes with perks like free shipping, special offers and more.Sign InShop by CategoryMenWomenKidsGolfOutdoorFollow us on socialCustomer ServiceAbout Us Services PoliciesYou have received this email to ahm203@yahoo.com, because you have signed up for our ECCO Newsletter. If you would prefer to no longer receive emails from ECCO please unsubscribe, here. This message was sent by: ECCO US, 16 Delta Drive, Londonderry, NH 03053.© ECCO. All rights reserved
"""
st = time.time()

prediction = classify_new_email(e1)
print("The new email is classified as:", prediction)
et = time.time()
time_taken = et - st
print("time taken: ", time_taken)
