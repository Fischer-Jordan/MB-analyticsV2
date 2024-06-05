import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Load your dataset
emails = pd.read_csv('invoice.csv')

# Assuming 'text' is the column containing email text and 'label' is the column containing labels (invoice or non-invoice)
X = emails['text']
y = emails['label']

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf_vectorizer.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Model Training (Logistic Regression)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Predictions
predictions = classifier.predict(X_test)

# Evaluation
print(classification_report(y_test, predictions))
print(f'Accuracy: {accuracy_score(y_test, predictions)}')

# Function to classify new emails
def classify_new_email(new_email):
    new_email_tfidf = tfidf_vectorizer.transform([new_email])
    prediction = classifier.predict(new_email_tfidf)
    return prediction[0]

# Example of classifying a new email
new_email = """
---------- Forwarded message ---------From: Swathi Mohan <swathi15mohan@gmail.com>Date: Fri, Dec 29, 2023 at 8:06 PMSubject: 
Fwd: redBus - Tax InvoiceTo: swathi.mohan@fischerjordan.com <swathi.mohan@fischerjordan.com>
---------- Forwarded message ---------From: redBus <no-reply@redbus.in>Date: Tue, 18 Jul 2023 at 13:14Subject: 
redBus - Tax InvoiceTo: <swathi15mohan@gmail.com>Dear Swathi Mohan ,Thank you for booking your ticket with redBus.
Ticket details:Ticket number (TIN): TS8F95973680From: BangaloreTo: Manipal* 
Bus operator is the primary service provider of passenger transportation services. redBus acts only 
as an intermediary for passenger transportation services. GST on passenger transportation services 
is collected and remitted by redBus in the capacity of E-commerce operator as per section 9(5) of the Central Goods and 
Services Act, 2017 and respective State GST Act. This invoice has been issued by redBus only with a limited purpose 
to comply with legal obligations as an e-commerce operator under GST law.Best,Team redBus


"""

new_email2="""
From: Newsletter Updates <info@dailynews.com>
Date: Mon, Oct 3, 2025 at 9:00 AM
Subject: Welcome to Daily News Updates

Dear Subscriber,

Thank you for subscribing to Daily News Updates! Get ready to receive a daily dose of top headlines, insightful articles, and breaking news directly to your inbox.

Stay informed, stay connected!

Best regards,
Daily News Updates Team

"""

new_email3="""
---------- Forwarded message ---------From: Swathi Mohan <swathi15mohan@gmail.com>Date: Fri, Dec 29, 2023 at 8:07 PM
Subject: Fwd: Your Swiggy order was delivered on timeTo: swathi.mohan@fischerjordan.com <swathi.mohan@fischerjordan.com>
---------- Forwarded message ---------From: Swiggy <noreply@swiggy.in>Date: Fri, 2 Dec 2022 at 13:52Subject: 
Your Swiggy order was delivered on timeTo: <swathi15mohan@gmail.com>Greetings from SwiggyYour order was delivered in 37 minutes! 
Rate this timely delivery hereOrder No:153042214009RestaurantThe Laughing BuddhaYour 
Order Summary:Order No: 153042214009Order placed at: Friday, December 2, 2022 1:13 PM
Order delivered at: Friday, December 2, 2022 1:51 PMOrder Status: DeliveredOrdered from:The Laughing Buddha
 D NO 2-7E , 7E1, 7E2, 7E3,7E4,7E5 , VIDYARATNA NAGAR , PERAMPALLI ROAD , MANIPAL , UDUPI,- 576104Delivery To:Swathi#5-77A 
 'Arch View', Temple Road, Indrali, UdupiIndrali Temple Rd, Hayagreeva Nagar, Udupi, Karnataka 576104,
   Indiahayagreeva nagar
   Item NameQuantityPricePeri Peri Wings 1₹ 280 
   Item Total: ₹ 280.00Delivery partner fee: ₹ 19.00Taxes: ₹ 14.00
   Order Total: ₹ 313
   The link to rate your delivery experience is only valid for mobile devices. 
   Disclaimer: Attached is the invoice for the restaurant services provided by the outlet. 
   For items not covered in the attached invoice, the outlet shall be responsible to issue an invoice directly to you. 
   Get the App: Follow us: ©2022-Swiggy. All rights reserved. Swiggy,Tower D, 9th Floor, IBC Knowledge Park, 
   Bannerghatta Road, Bangalore - 560029 

"""

prediction = classify_new_email(new_email3)
print("The new email is classified as:", prediction)