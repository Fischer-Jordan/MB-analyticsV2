import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import os
import pandas as pd

def count_emojis(text):
    return emoji.emoji_count(text)

invoice_indicative_keywords = [
    "invoice #", "order number", "order #", "invoice", "purchase", "hsn code", "bill to", "total invoice value", "ship to",
    "address", "tax invoice", "order id", "receipt", "billing", "payment", "transaction", "due date", "amount due",
    "credit", "debit", "account statement", "balance", "invoice date", "payment due", "total amount", "payable",
    "purchase order", "confirmation", "shipping", "tracking", "shipment", "dispatch", "delivery", "order confirmation",
    "receipt number", "payment details", "invoice total", "itemized bill", "order"
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
    svm_model_path = "svm_model_subject_discount.joblib"
    tfidf_vectorizer_path = "tfidf_vectorizer_subject_discount.joblib"
    
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
    confidence_spam = confidence_scores[0][1]
    confidence_promotion = confidence_scores[0][2]
    confidence_discount = confidence_scores[0][3]
    
    final_prediction = post_process_predictions(new_email, prediction[0], emoji_count)

    # unload models
    del loaded_svm_model
    del loaded_tfidf_vectorizer

    return final_prediction, confidence_invoice, confidence_spam, confidence_promotion, confidence_discount

def classify_emails_from_csv(input_csv_path, output_csv_path):
    # Read the CSV file
    df = pd.read_csv(input_csv_path)

    # Check if the 'subject' column exists
    if 'subject' not in df.columns:
        raise ValueError("The input CSV file must contain a 'subject' column.")

    # Classify each subject and add the predictions and confidence scores to new columns
    df['prediction'] = ''
    df['confidence_invoice'] = 0.0
    df['confidence_spam'] = 0.0
    df['confidence_promotion'] = 0.0
    df['confidence_discount'] = 0.0
    
    for index, row in df.iterrows():
        subject = row['subject']
        prediction, confidence_invoice, confidence_spam, confidence_promotion, confidence_discount = classify_email(subject)
        df.at[index, 'prediction'] = prediction
        df.at[index, 'confidence_invoice'] = confidence_invoice
        df.at[index, 'confidence_spam'] = confidence_spam
        df.at[index, 'confidence_promotion'] = confidence_promotion
        df.at[index, 'confidence_discount'] = confidence_discount

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"Predictions and confidence scores saved to {output_csv_path}")

# Example usage
input_csv_path = "email_subjects.csv"
output_csv_path = "output_email_subjects.csv"
classify_emails_from_csv(input_csv_path, output_csv_path)
