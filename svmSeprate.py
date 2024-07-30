import pandas as pd
# import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix   # noqa
import joblib

print('nltk downloaded')


def preprocess(text):
    text = str(text).lower().replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')  # noqa
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # noqa
    return text


# Load your dataset
datapath = "/Users/harsh/Workspace/FJStuff/ScrapeMB/manuallyLabeledDIPSData.csv"
emails = pd.read_csv(datapath, encoding='ISO-8859-1').drop_duplicates()  # noqa
emails['text']=emails['body']
emails['label']=emails['label'].apply(lambda x: 'invoice' if x=='shipping' else x)
#emails = emails.groupby('label').head(60)
emails = emails.reset_index(drop=True)

lbls = ['invoice','promotion','discount']
for y in lbls:
	emails[y]=emails['label'].apply(lambda x: y if x==y else f'not_{y}')

print('read dataset')
emails['text'] = emails['text'].replace({'\r\n': ' ', '\n': ' ', '\r': ' '}, regex=True)  # noqa
emails['text'] = emails['text'].apply(preprocess)


# Function to count emojis
def count_emojis(text):
    return emoji.emoji_count(text)


invoice_indicative_keywords = [
    'invoice #', 'order number', 'order #', 'invoice', 'purchase', 'hsn code', 
    'bill to', 'total invoice value', 'ship to', 'address',
    'tax invoice', 'order id', 'receipt', 'billing', 'payment', 'transaction',
    'due date', 'amount due',
    'credit', 'debit', 'account statement', 'balance', 'invoice date',
    'payment due', 'total amount', 'payable', 'purchase order', 'confirmation',
    'shipping', 'tracking', 'shipment', 'dispatch', 'delivery',
    'order confirmation',
    'receipt number', 'payment details', 'invoice total', 'itemized bill',
    "Delivered", "Total paid", "Items ordered"
]

emails['exclamation_mark_count'] = emails['text'].apply(lambda text: text.count('!'))  # noqa
emails['has_invoice_keyword'] = emails['text'].apply(lambda text: any(keyword in text for keyword in invoice_indicative_keywords))  # noqa
emails['numeric_count'] = emails['text'].apply(lambda text: sum(c.isdigit() for c in text))  # noqa
emails['percentage_sign_count'] = emails['text'].apply(lambda text: text.count('%'))  # noqa
emails['dollar_symbol_count'] = emails['text'].apply(lambda text: text.count('$'))  # noqa
emails['rupee_symbol_count'] = emails['text'].apply(lambda text: text.count('₹'))  # noqa
emails['emoji_count'] = emails['text'].apply(count_emojis)

# Feature Extraction with TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), max_df=0.95, min_df=2)  # noqa
X_tfidf = tfidf_vectorizer.fit_transform(emails['text'])
X_extra = emails[['exclamation_mark_count', 'has_invoice_keyword',
                  'numeric_count',
                  'percentage_sign_count', 'dollar_symbol_count',
                  'rupee_symbol_count', 'emoji_count']].values
X_combined = pd.concat([pd.DataFrame(X_tfidf.toarray()), pd.DataFrame(X_extra)], axis=1)  # noqa
y = emails[lbls].reset_index(drop=True)
#y = emails['label']

print('vectorization done')
out=pd.DataFrame()

# Train-Test Split
tmp = X_combined.copy()
tmp['text'] = emails['text']
tmp[y.columns]=y
tmp = tmp.reset_index(drop=True)
#tmp = tmp.groupby('lbl').head(60).reset_index(drop=True)

X_train, X_test, y_train_full, y_test_full = train_test_split(tmp.drop(columns=y.columns), tmp[y.columns], test_size=0.2, random_state=42) # noqa
print('training testing split done')

# Model Training (SVM)

for x in lbls:
	y_train = y_train_full[x]
	y_test = y_test_full[x]

	svm_classifier = SVC(kernel='linear', probability=False) # True)
	svm_classifier.fit(X_train.drop(columns='text'), y_train)
	print('classifer loaded')
	
	# Predictions
	predictions_svm = svm_classifier.predict(X_test.drop(columns='text'))
	predictions_svm_train = svm_classifier.predict(X_train.drop(columns='text'))

	tmp[f'pred_{x}'] = svm_classifier.predict(tmp.drop(columns=[x for x in tmp.columns if type(x)==str]))
	print('predicted')

	#joblib.dump(svm_classifier, f'modelv4/svm_model_{x}.joblib')
	#joblib.dump(tfidf_vectorizer, f'modelv4/tfidf_vectorizer_{x}.joblib')
	
	print('model dumped')
	# Evaluation
	print("SVM Classifier Results Test: ")
	print(classification_report(y_test, predictions_svm))
	print(f'Accuracy: {accuracy_score(y_test, predictions_svm)}')
	print()
	
	
	conf_matrix = confusion_matrix(y_test, predictions_svm, labels=[f'{x}', f'not_{x}'])  # noqa
	print("Confusion Matrix on Testing dataset:")
	print(pd.DataFrame(conf_matrix, index=[f'Actual {x}', f'Actual not_{x}'],  # noqa
                   columns=[f'Predicted {x}', f'Predicted not_{x}']))  # noqa
	
	print("SVM Classifier Results Train: ")
	print(classification_report(y_train, predictions_svm_train))
	print(f'Accuracy: {accuracy_score(y_train, predictions_svm_train)}')
	print()
	
	conf_matrix = confusion_matrix(y_train, predictions_svm_train, labels=[f'{x}', f'not_{x}'])  # noqa
	print("Confusion Matrix on Train dataset:")
	print(pd.DataFrame(conf_matrix, index=[f'Actual {x}', f'Actual not_{x}'],  # noqa
                   columns=[f'Predicted {x}', f'Predicted not_{x}']))  # noqa

tmp[['text','invoice','promotion','discount','pred_invoice','pred_promotion','pred_discount']].to_csv('svmSeprateOut.csv')
