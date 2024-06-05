import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import os
import pandas as pd
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
def classify_subject(new_email):
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
    confidence_invoice = confidence_scores[0][0]*100
    confidence_spam=confidence_scores[0][1]*100
    # print('prediction: ', prediction)
    # print(f"confidence %invoice:  {confidence_invoice*100} ")
    # print(f"confidence %spam:  {confidence_spam*100}")
    
    final_prediction = post_process_predictions(new_email, prediction[0], emoji_count)

    # unload models
    del loaded_svm_model
    del loaded_tfidf_vectorizer

    return [final_prediction,confidence_invoice, confidence_spam] 



def classify_email(new_email):
    # Load the pre-trained model and vectorizer
    svm_model_path =  "svm_model_new.joblib"
    tfidf_vectorizer_path = "tfidf_vectorizer_new.joblib"
    
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
    confidence_invoice = confidence_scores[0][0]*100
    confidence_spam=confidence_scores[0][1]*100
    # print('prediction: ', prediction)
    # print(f"confidence %invoice:  {confidence_invoice*100} ")
    # print(f"confidence %spam:  {confidence_spam*100}")
    
    final_prediction = post_process_predictions(new_email, prediction[0], emoji_count)

    # unload models
    del loaded_svm_model
    del loaded_tfidf_vectorizer

    return [final_prediction,confidence_invoice, confidence_spam] 



def decide(e, sub):
    prediction_subject, invoice_confidence_subject, spam_confidence_subject=classify_email(e)
    prediction_email, invoice_confidence_email, spam_confidence_email=classify_subject(sub)
    
    if prediction_email == prediction_subject:
        prediction= prediction_email
    else:
        if prediction_subject == 'invoice' and prediction_email == 'spam':
            if invoice_confidence_subject > spam_confidence_email:
                prediction= 'invoice'
            else:
                prediction= 'spam'
        elif prediction_subject == 'spam' and prediction_email == 'invoice':
            if spam_confidence_subject > invoice_confidence_email:
                prediction= 'spam'
            else:
                prediction= 'invoice'
    return prediction, invoice_confidence_subject,spam_confidence_subject, invoice_confidence_email, spam_confidence_email

def process_emails(csv_file_path):
    emails_df = pd.read_csv(csv_file_path, encoding='latin1')
    predictions = []
    invoice_confidence_subjects=[]
    spam_confidence_subjects=[]
    invoice_confidence_emails=[]
    spam_confidence_emails=[]
    
    for index, row in emails_df.iterrows():
        email = row['text']
        subject = row['subject']
        prediction, invoice_confidence_subject,spam_confidence_subject, invoice_confidence_email, spam_confidence_email = decide(email,subject)
        predictions.append(prediction)
        invoice_confidence_subjects.append(invoice_confidence_subject)
        spam_confidence_subjects.append(spam_confidence_subject)
        invoice_confidence_emails.append(invoice_confidence_email)
        spam_confidence_emails.append(spam_confidence_email)

    # Add predictions to DataFrame and save to new CSV
    emails_df['label'] = predictions
    emails_df['subject_invoice']=invoice_confidence_subjects
    emails_df['subject_spam']=spam_confidence_subjects
    emails_df['email_invoice']=invoice_confidence_emails
    emails_df['email_spam']=spam_confidence_emails
    emails_df.to_csv('classified_sub_and_email.csv', index=False)

process_emails('classified_sub_and_email.csv')
