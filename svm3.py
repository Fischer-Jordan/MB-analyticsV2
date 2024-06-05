import pandas as pd
import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Preprocessing function
def preprocess(text):
    text = str(text).lower().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

# Load your dataset
emails = pd.read_csv('updated_balanced_dataset.csv', encoding='ISO-8859-1').drop_duplicates()
emails['text'] = emails['text'].apply(preprocess)
emails['subject'] = emails['subject'].apply(preprocess)
emails['combined_text'] = emails['text'] + " " + emails['subject']

# Define invoice-indicative keywords
invoice_indicative_keywords = [
    'invoice #', 'order number', 'order #', 'invoice', 'purchase',
    'HSN Code', 'Bill to/Ship to', 'Total invoice value'
]

# Count emojis in the combined text
def count_emojis(text):
    return emoji.emoji_count(text)

# Adding additional features
emails['exclamation_mark_count'] = emails['combined_text'].apply(lambda text: text.count('!'))
emails['has_invoice_keyword'] = emails['combined_text'].apply(lambda text: any(keyword in text for keyword in invoice_indicative_keywords))
emails['numeric_count'] = emails['combined_text'].apply(lambda text: sum(c.isdigit() for c in text))
emails['percentage_sign_count'] = emails['combined_text'].apply(lambda text: text.count('%'))
emails['dollar_symbol_count'] = emails['combined_text'].apply(lambda text: text.count('$'))
emails['rupee_symbol_count'] = emails['combined_text'].apply(lambda text: text.count('₹'))
emails['emoji_count'] = emails['combined_text'].apply(count_emojis)

# Feature Extraction with TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), max_df=0.95, min_df=2)
X_tfidf = tfidf_vectorizer.fit_transform(emails['combined_text'])
X_extra = emails[['exclamation_mark_count', 'has_invoice_keyword', 'numeric_count',
                  'percentage_sign_count', 'dollar_symbol_count', 'rupee_symbol_count', 'emoji_count']].values
X_combined = pd.concat([pd.DataFrame(X_tfidf.toarray()), pd.DataFrame(X_extra)], axis=1)

# Define labels
y = emails['label']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Model Training (SVM)
svm_classifier = SVC(kernel='linear')  # You can choose different kernels like 'linear', 'rbf', etc.
svm_classifier.fit(X_train, y_train)

# Predictions
predictions_svm = svm_classifier.predict(X_test)

# Save the model and vectorizer
joblib.dump(svm_classifier, 'svm_model_subject.joblib')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer_subject.joblib')

# Evaluation
print("SVM Classifier Results:")
print(classification_report(y_test, predictions_svm))
print(f'Accuracy: {accuracy_score(y_test, predictions_svm)}')

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, predictions_svm, labels=['ham', 'invoice', 'spam'])
print("Confusion Matrix on Testing dataset:")
print(pd.DataFrame(conf_matrix, index=['Actual ham', 'Actual invoice', 'Actual spam'], columns=['Predicted ham', 'Predicted invoice', 'Predicted spam']))

# Function to classify new emails
def classify_new_email(new_email, new_subject):
    combined_input = preprocess(new_email) + " " + preprocess(new_subject)
    tfidf_features = tfidf_vectorizer.transform([combined_input])
    feature_vector = tfidf_features.toarray()[0].tolist()
    feature_vector.extend([
        combined_input.count('!'),
        int(any(keyword in combined_input.lower() for keyword in invoice_indicative_keywords)),
        sum(c.isdigit() for c in combined_input),
        combined_input.count('%'),
        combined_input.count('$'),
        combined_input.count('₹'),
        count_emojis(combined_input)
    ])
    prediction = svm_classifier.predict([feature_vector])
    return prediction[0]
