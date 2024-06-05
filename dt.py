import pandas as pd
import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

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
emails = pd.read_csv('balanced_dataset.csv', encoding='ISO-8859-1').drop_duplicates()
emails['text'] = emails['text'].replace({'\r\n': ' ', '\n': ' ', '\r': ' '}, regex=True)
emails['text'] = emails['text'].apply(preprocess)

# Function to count emojis
def count_emojis(text):
    return emoji.emoji_count(text)

invoice_indicative_keywords = [
    'invoice #', 'order number', 'order #', 'invoice', 'purchase',
    'HSN Code', 'Bill to/Ship to', 'Total invoice value'
]

emails['exclamation_mark_count'] = emails['text'].apply(lambda text: text.count('!'))
emails['has_invoice_keyword'] = emails['text'].apply(lambda text: any(keyword in text for keyword in invoice_indicative_keywords))
emails['numeric_count'] = emails['text'].apply(lambda text: sum(c.isdigit() for c in text))
emails['percentage_sign_count'] = emails['text'].apply(lambda text: text.count('%'))
emails['dollar_symbol_count'] = emails['text'].apply(lambda text: text.count('$'))
emails['rupee_symbol_count'] = emails['text'].apply(lambda text: text.count('₹'))
emails['emoji_count'] = emails['text'].apply(count_emojis)

# Feature Extraction with TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), max_df=0.95, min_df=2)
X_tfidf = tfidf_vectorizer.fit_transform(emails['text'])
X_extra = emails[['exclamation_mark_count', 'has_invoice_keyword', 'numeric_count',
                  'percentage_sign_count', 'dollar_symbol_count', 'rupee_symbol_count', 'emoji_count']].values
X_combined = pd.concat([pd.DataFrame(X_tfidf.toarray()), pd.DataFrame(X_extra)], axis=1)

y = emails['label']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Model Training (Decision Tree)
decision_tree_classifier = DecisionTreeClassifier()
decision_tree_classifier.fit(X_train, y_train)

# Predictions
predictions_dt = decision_tree_classifier.predict(X_test)
wrongly_classified_indices = (y_test == 'invoice') & (predictions_dt != 'invoice')

# Extract wrongly classified emails
wrongly_classified_emails = emails.loc[X_test.index[wrongly_classified_indices], 'text']

# Print or analyze wrongly classified emails
print("Wrongly Classified Emails:")
print(wrongly_classified_emails)

# Evaluation
print("Decision Tree Classifier Results:")
print(classification_report(y_test, predictions_dt))
print(f'Accuracy: {accuracy_score(y_test, predictions_dt)}')
print()


# predictions_total = decision_tree_classifier.predict(X_combined)
# conf_matrix_total = confusion_matrix(y, predictions_total, labels=['ham', 'invoice', 'spam'])
# labels_total = ['Actual ham', 'Actual invoice', 'Actual spam']
# print("Confusion Matrix on the Entire Dataset:")
# print(pd.DataFrame(conf_matrix_total, index=['Actual ham', 'Actual invoice', 'Actual spam'], columns=['Predicted ham', 'Predicted invoice', 'Predicted spam']))
# print()


conf_matrix = confusion_matrix(y_test, predictions_dt, labels=['ham', 'invoice', 'spam'])
print("Confusion Matrix:")
print(pd.DataFrame(conf_matrix, index=['Actual ham', 'Actual invoice', 'Actual spam'], columns=['Predicted ham', 'Predicted invoice', 'Predicted spam']))

def classify_new_email(new_email, tfidf_vectorizer, classifier):
    preprocessed_email = preprocess(new_email)
    tfidf_features = tfidf_vectorizer.transform([preprocessed_email])
    exclamation_mark_count = preprocessed_email.count('!')
    has_invoice_keyword = any(keyword in preprocessed_email.lower() for keyword in invoice_indicative_keywords)
    numeric_count = sum(c.isdigit() for c in preprocessed_email)
    percentage_sign_count = preprocessed_email.count('%')
    dollar_symbol_count = preprocessed_email.count('$')
    rupee_symbol_count = preprocessed_email.count('₹')
    emoji_count = count_emojis(preprocessed_email)
    
    # Create a feature vector
    feature_vector = tfidf_features.toarray()[0].tolist()
    feature_vector.extend([exclamation_mark_count, int(has_invoice_keyword), numeric_count,
                           percentage_sign_count, dollar_symbol_count, rupee_symbol_count, emoji_count])
    
    # Make a prediction
    prediction = classifier.predict([feature_vector])
    return prediction[0]

def post_process_predictions(texts, predictions):
    """
    Post-process the predictions based on the presence of invoice-indicating keywords.
    :param texts: The original texts of the emails.
    :param predictions: The predicted labels.
    :return: The post-processed predicted labels.
    """
    processed_predictions = []
    for text, prediction in zip(texts, predictions):
        if any(keyword in text.lower() for keyword in invoice_indicative_keywords):
            processed_predictions.append('invoice')  # Override prediction if keywords are found
        else:
            processed_predictions.append(prediction)
    return processed_predictions




# Example of classifying a new email
e1="""
---------- Forwarded message ---------From: <donotreply-bbinstant@bigbasket.com>Date: Thu, 29 Jun 2023 at 17:51Subject: Your purchase with Big Basket InstantTo: <paramkapur2002@gmail.com>ORIGINAL TAX INVOICE Bill to/Ship to: Invoice NoKA23K-0001025153Order IDBBYANW1688041299Date of Issue of Invoice29.06.23 05:51 PMFinal Total Rs. 90.00 No of Items 3 Innovative Retail Concepts Pvt Ltd #214/c, D.R Munireddy industrial area Doddanakkundi bangalore-560037 Karnataka (29) Tel.: +1860 123 1000 GSTIN : 29AACCI2053A1Z3 CIN : U74130KA2010PTC052192 Sl NoItem DescriptionHSN Code/SACQuantity,along with unitsTotal Value,for supply of goods1 Pepsi Soft Drink - Black, 250 ml 513 2 70 2 Cadbury Dairy Milk Chocolate, 23 gms 2751 1 20 Total Rs. 90.00 * Inclusive of all taxes Total invoice value (In Figure) : Rs. 90.00 Print As per Section 31 of CGST Act read with Rules, invoice is issued at the point of delivering the goods Click here to unsubscribe

"""

e2="""
---------- Forwarded message ---------From: The Economic Times <newsletter@notifications-economictimes.com>Date: Mon, 25 Dec 2023 at 14:50Subject: Join the Crypto Academy's first episode as we unravel the investment landscape in the aftermath of the bull runTo: <swathi15mohan@gmail.com> Dear Reader, Greetings from EconomicTimes.com! The Economic Times is excited to bring the maiden episode of Crypto Academy—a virtual webinar series—yet another initiative as part of its dedicated Crypto section, to make the world of crypto accessible to a wider audience. What to expect from this session :Data-led insights that will help novice and seasoned investors make sharper decisions on the industry's current state and potential scaleDeep dive into crypto's post bull-run landscape and get expert assessment of risks and rewardsUnderstand dynamics that shape the value of cryptos and why certain cryptocurrencies command higher prices Explore the impact of regulatory perspectives on crypto trades & potential challenges and opportunities for investors.Date - 27th December 2023Time - 3 PMREGISTER NOW TO JOIN!Join Edul Patel, Co-founder & CEO of Mudrex , and Ajeet Khurana, Ex-CEO, Zebpay, in conversation with Apoorva Mittal, Special Correspondent, The Economic Times in the first episode of Crypto Academy Last year the market came out of a bull run that left a bloodbath behind with key crypto institutions falling and investors suffering massive losses. It is against this backdrop that these experts will shed light on the topic ‘How to navigate through the crypto bull run’. If you are interested in learning more about crypto investments, do not miss this opportunity to deep dive into the post-bull-run landscape and sharpen your understanding of the dynamics that determine the value of cryptos, the meme coin buzz, and more. Best Regards, Economictimes.com To ensure that you continue receiving emails, please add verification@economictimes.com to your address book.Copyright © 2023 Bennett, Coleman & Co. Ltd. All rights reserved.If you don’t wish to receive this mailer, click here to Unsubscribe from our mailing list. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

"""

e3="""
---------- Forwarded message ---------From: Param Kapur <param.kapur@fischerjordan.com>Date: Fri, Jan 5, 2024 at 7:29 PMSubject: MyBrands Meeting 1/5To: Anthony Mavromatis <ahm203@gmail.com>, Boaz Salik <boaz.salik@fischerjordan.com>, Om Avhad <om.avhad@fischerjordan.com>, Yash Mundra <yash.mundra@fischerjordan.com>, Swathi Mohan <swathi.mohan@fischerjordan.com>, Khushi Bhatia <khushi.bhatia@fischerjordan.com>Hey team, Happy Friday! I have created an informal meeting agenda that will give us some structure for an update. Looking forward to our discussion. Recap from last meetingPDF invoice scanning is now deployed, you can send a PDF as an attachment and it will be read inCategories for Items and Vendors has been added to the model Ticket has been created for Khushi to add the dropdown of ItemCategories in the frontendFetch Amazon connection Found an Amazon program that allows Login with Amazon through a contact. Have experimented with it a bit – need to find out if past order data is exposed through that APIOCR Model Swathi has completed step 1 of OCR model Bounding boxes are being drawn around the text of the receipt DemoNext Step: Using an existing dataset create a fine-tune of LayoutLM OCR that will process the bounding box text data to extract with structurePre-processingBounding box around receipt is being drawn for images without additional text Using MSER and Image optimization techniques Issue: Images of receipts with many background features confuse the model and the bounding box is not properly drawn. Solution: On the frontend, the camera should have a rectangular box overlayed in which users must fit the receipt. This box then initially crops the receipt so that the model has a better time of drawing a bounding box. Aside: JPMorgan released a paper on DocLLM: might be a guiding light for our future LLM model. “Enterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively.” https://arxiv.org/pdf/2401.00908.pdfNext Steps:Get Khushi started on backlog of tickets Would be helpful if we can prioritize these tickets by urgency Continue work on OCR preprocessing as plannedContinue work on OCT model as plannedSandbox Login with Amazon API to discover what data is exposed through itBest, Param -- Param Kapur FischerJordan +91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If you are not an intended recipient of this email, please immediately notify the sender by replying to this email, delete the message and any attachments from your account, and do not forward or otherwise distribute the message or any attachments.

"""


prediction = classify_new_email(e1, tfidf_vectorizer, decision_tree_classifier)
# print("The new email is classified as:", prediction)