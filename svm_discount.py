# import pandas as pd
# import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib


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
    text = str(text).lower().replace("\r\n", " ").replace("\n", " ").replace("\r", " ")  # noqa
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    text = " ".join(
        [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]  # noqa
    )
    return text


# Load the pre-trained model and vectorizer
loaded_svm_model = joblib.load("svm_model_discount.joblib")
loaded_tfidf_vectorizer = joblib.load("tfidf_vectorizer_discount.joblib")


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
Dear John Doe,
I hope this email finds you well.
Please find attached the invoice #4567 for your web hosting \
services for the month of May 2024. The total amount due is \
$120.00, payable by June 15, 2024.
Should you have any questions regarding this invoice, \
please do not hesitate to contact us.
Thank you for your prompt attention to this matter.
Best regards,
TechHost Solutions
Billing Department
"""

e2 = """
Dear Lucky Winner,
Congratulations! You have been selected to receive a free cruise trip to the \
Bahamas. This once-in-a-lifetime opportunity is yours to claim!
Click the link below to provide your details and secure your spot on this \
fabulous journey:
Hurry, this offer is valid for a limited time only!
Best wishes,
The Free Cruise Team
"""

e3 = """
Dear Jane Smith,
I hope this message finds you well.
We are thrilled to inform you about an exciting career opportunity at \
BrightFuture Marketing. We are currently looking for talented individuals to \
join our dynamic marketing team.
If you are passionate about marketing and looking for a challenging yet \
rewarding role, we would love to hear from you. Please visit our careers page \
for more information and to apply.
Best regards,
Anna Johnson
HR Manager
BrightFuture Marketing
"""

e4 = """
Dear Valued Customer,
We are excited to offer you an exclusive 20% discount on all electronics at \
TechMart! This limited-time offer is our way of saying thank you for being \
a loyal customer.
To take advantage of this discount, simply use the code TECH20 at checkout. \
Hurry, this offer is valid until June 30, 2024.
Happy shopping!
Best regards,
TechMart Sales Team
"""

e5 = """
Dear Emily,
Get ready for summer with our incredible Flash Sale! This weekend only, enjoy \
50% off all summer clothing at SunnyStyles. From dresses and shorts to \
swimwear and accessories, we've got everything you need to look fabulous this \
season.
Don't miss out on these unbeatable deals! Shop online or visit our stores \
from \
May 30 to June 1 to take advantage of this exclusive offer.
Use promo code SUMMER50 at checkout to apply your discount.
Happy shopping!
Best regards,
SunnyStyles Sales Team
"""

e6 = """
Dear Ravi Sharma,
We are excited to announce a groundbreaking update for all tech enthusiasts! \
Our new SmartRouter was recently showcased at the Tech Innovators Expo, \
highlighting its seamless integration with all smart home devices.
With our latest SmartRouter, connecting to Wi-Fi has never been easier. Forget\
the complicated setup processes of the past. Now, all you need to do is plug \
in the SmartRouter, and it automatically configures to provide you with \
lightning-fast internet speeds.
Enjoy uninterrupted streaming, gaming, and browsing with the latest in Wi-Fi \
technology. Our SmartRouter ensures you have a stable and \
secure connection at all times.
Ready to upgrade your home network? Visit our website to learn more about the \
SmartRouter and how it can transform your internet experience.
Stay connected effortlessly!
Best regards,
TechNet Innovations Team
"""

e7 = """
Hello Alex, Indulge in a unique experience at our exclusive event. Our expert \
chef has crafted a new menu that celebrates the finest ingredients. \
Join us for an evening of gourmet delights. \
Savor the moment,
The TechWorld Team

"""
prediction = classify_new_email(e1)
print(f"--------------------\n{e1}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e2)
print(f"--------------------\n{e2}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e3)
print(f"--------------------\n{e3}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e4)
print(f"--------------------\n{e4}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e5)
print(f"--------------------\n{e5}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e6)
print(f"--------------------\n{e6}\nThe new email is classified as: {prediction}")  # noqa

prediction = classify_new_email(e7)
print(f"--------------------\n{e7}\nThe new email is classified as: {prediction}")  # noqa
