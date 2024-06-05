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
]


def post_process_predictions(email, prediction, emoji_count):
    email_lower = email.lower()
    matching_keywords = [
        keyword
        for keyword in invoice_indicative_keywords
        if keyword.lower() in email_lower
    ]
    keyword_count = len(matching_keywords)
    if keyword_count > 10 and prediction != "invoice":
        return "invoice"
    if emoji_count > 5 and prediction in ["ham", "invoice"]:
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

e1="""
 Hello Anthony, Thank you for shopping with us. We’ll send a confirmation when your items ship. Your purchase has been divided into 3 orders. Order Confirmation Arriving: tomorrow, May 6 Ship to: Anthony BROOKLYN, NY Order # 112-9719790-9933000 View or manage order USimplySeason Zaatar Spice ... Qty : 1 Vegan D3 + K2 Organic 100% ... Qty : 1 Pentel GraphGear 500 Automa... Qty : 3 Order Total: $82.15 Order Confirmation Arriving: Wednesday, May 8 Ship to: Anthony BROOKLYN, NY Order # 112-9739103-5127468 View or manage order Nutri-Align Fasting Salts E... Qty : 1 Chandrika Bath and Body Ayu... Qty : 1 Pentel GraphGear 500 Automa... Qty : 1 Order Total: $62.23 Order Confirmation Arriving: Sunday, May 12 - Tuesday, May 14 Ship to: Anthony BROOKLYN, NY Order # 112-8953254-4310634 View or manage order Muay Thai Kick Boxing Gear ... Qty : 1 Order Total: $25.03 Keep shopping forBadger Coral Reef Safe Sunscreen Tin,...$13.59FellDen Micro Solar Panels with Wire,...$15.99 The payment for your invoice is processed by Amazon Payments, Inc. P.O. Box 81226 Seattle, Washington 98108-1226. If you need more information, please contact (866) 216-1075 By placing your order, you agree to Amazon.com’s Privacy Notice and Conditions of Use. Unless otherwise noted, items sold by Amazon.com are subject to sales tax in select states in accordance with the applicable laws of that state. If your order contains one or more items from a seller other than Amazon.com, it may be subject to state and local sales tax, depending upon the seller's business policies and the location of their operations. Learn more about tax and seller information. This email was sent from a notification-only address that cannot accept incoming email. Please do not reply to this message. 
 """
 
 
e2="""
 Hi Boaz, Your package has been delivered! How was your delivery? It was great Not so great Order # 113-7166023-8865007 Track your package Return or replace items in Your Orders. This email was sent from a notification-only email address that cannot accept incoming email. Please do not reply to this message. © 2019 Amazon.com, Inc. or its affiliates. All rights reserved. Amazon, Amazon.com, and the Amazon.com logo are registered trademarks of Amazon.com, Inc. or its affiliates. Amazon.com, 410 Terry Avenue N., Seattle, WA 98109-5210 
 
 """

e3="""
Reebok Going going… ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ VIEW IN BROWSERPrices are marked. Valid thru 5/5. Exclusions apply. Shop Now FREE SHIPPING ON ORDERS OF $75 OR MOREMY ACCOUNTFIND A STORENEED HELP?Free ground shipping offer on orders of $75 or more valid to U.S. addresses only. All offers valid on domestic U.S. orders only.This email was sent to: erinsalik@gmail.comUnsubscribe and Manage My Preferences | Contact Us | Privacy Policy This email was sent by: Reebok International Ltd., LLC | 25 Drydock Ave. | Boston, MA 02210 | United States © 2024 Reebok. All Rights Reserved. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
 
"""

e4="""
Order Confirmation - Paleovalley.comHi Anthony,Thank you for placing your order with us!Please look for a follow up email from within the next 2 business days that will contain your tracking information.Your order details are:Order Id - 3477952 (View Invoice)Item PVBS - 100% Grass Fed Beef Sticks (10 Pack), Qty - 4Item Total - $89.96Flavor: OriginalItem PVCSB - Pasture-Raised Chicken Sticks, Qty - 1Item Total - $24.99Flavor: BuffaloItem PVVSO - 100% Grass Fed Venison Sticks, Qty - 1Item Total - $24.99Flavor: OriginalSales Tax: $0.00Shipping Total: $0.00Order Total: $139.94Shipping Details:Name - Anthony MavromatisAddress - 41 4th PlaceAddress2 - Groud Level Red DoorCity - BrooklynState - NYCountry - USPostcode - 11231Please contact us if any of the above details appear incorrect.Join The Paleovalley Facebook Page for more updates, articles, and deals at the link below:You'll see a Like button on the cover photo near the bottom right > Click it.I can’t wait to help you lose weight, eliminate nagging joint pain and inflammation, heal your gut, sleep better, have lasting energy throughout the day and living a life of optimal health! I look forward to helping you experience all these amazing results and more.At Paleovalley we love hearing from our customers! So if you have ANY comments, questions, or feedback, PLEASE don't hesitate to let us know! The fastest way to get your questions answered is to shoot the Paleovalley team a quick email on our Contact Page or directly at: support@paleovalley.com and we'll get back to you quickly. (We’re here from Monday – Saturday from 8am – 7pm PST) - However, we love to make our customers as happy as possible, so we usually check emails around the clock, so feel free to email us at anytime. :-)To Your Success!The Paleovalley Teamunsubscribe  

"""

e5="""
Your transfer's completeIf you’d like to see your account balance, just sign in. Sign InYour transfer’s complete.Hi Anthony H Mavromatis,Your money has transferred.Amount: $423.00From: 360 Savings...0797To: MONEY...8752Memo: Transferred On: May 5, 2024Available On: May 5, 2024Your confirmation number is MM8ZU7J0YKVM38V.To see your account balance, sign in.Thanks.Download the mobile app.About this messageThe site may be unavailable during normal maintenance or due to unforeseen circumstances. Important information from Capital OneContact us | Privacy | Help prevent fraudTo ensure delivery, add capitalone@notification.capitalone.com to your address book.This email was sent to ahm203@yahoo.com and contains information directly related to your account with us, other services to which you have subscribed, and/or any application you may have submitted.Capital One does not provide, endorse or guarantee any third-party product, service, information or recommendation listed above. The third parties listed are not affiliated with Capital One and are solely responsible for their products and services. All trademarks are the property of their respective owners.Please do not reply to this message, as this email inbox is not monitored. To contact us, visit www.capitalone.com/help-center/contact-us.Products and services are offered by Capital One, N.A., Member FDIC.© 2024 Capital One. Capital One is a federally registered service mark.TRNCOM 43540 10823

"""

e6="""
Lilly PulitzerMother's Day is in one week! Free shipping and returns | Shop NowNew ArrivalsPrintsDressesSwimShoes & Accessories CONNECT STORESUnsubscribe Manage My Account Contact Us Privacy Policy ©2024 Lilly Pulitzer 800 3rd Ave, King of Prussia, PA 19406View in Browser 800 3rd Ave King of Prussia, PA 19406 US Manage Subscriptions | Update Profile | Unsubscribe © 2024 Lilly Pulitzer 

"""

e7="""
Shipping Confirmation Hello Boaz, We wanted to let you know that we have shipped your items. Shipping Confirmation Your package will arrive by Sunday, May 5 Ship to Boaz REDONDO BEACH, CA Order # 113-7166023-8865007 Track package An Amazon driver may contact you by text message or call you for help on the day of delivery. Shipment total $12.02 Return or replace items in Your orders Learn how to recycle your packaging at Amazon Second Chance. Keep shopping forUgerlov Women's Tennis Dress Summer...$38.99Logitech C270 HD Webcam, 720p,...$17.99 Unless otherwise noted, items sold by Amazon.com are subject to sales tax in select states in accordance with the applicable laws of that state. If your order contains one or more items from a seller other than Amazon.com, it may be subject to state and local sales tax, depending upon the sellers business policies and the location of their operations. Learn more about tax and seller information. Your invoice can be accessed here. One or more items in your shipment was supplied by a different seller than the seller you purchased the item from. Visit Your Orders from a web browser to see the suppliers of these items on your invoices. This email was sent from a notification-only address that cannot accept incoming email. Do not reply to this message. 

"""

e8="""
Sam EdelmanShop New Arrivals | View the email in your browser. © 2024 Sam Edelman. All Rights Reserved. You are receiving this message because you opted-in your email address erinsalik@gmail.com to receive emails from samedelman.com. If you would like to be removed from our mailing list, please unsubscribe here. | View our privacy policy. To ensure ongoing optimal receipt of these communications, please add reply@email.samedelman.com to your address book. If, for any reason, this promotion is not capable of running as planned, sponsor reserves the right to cancel, terminate, modify or suspend the promotion. This includes, but is not limited to, infection by computer virus, bugs, tampering, unauthorized intervention, fraud, technical failures or any other causes beyond the control of the sponsor.samedelman.com | 8300 Maryland Ave. | St. Louis, MO 63105 USA © 2024 Caleres, Inc. 

"""

e9="""
 Vans To view this email as a web page, click here. Hi Erin, We are working on your order 86989803. Please allow additional processing time for orders placed after 11am PST. We will email you a shipping confirmation once it is on the way. If you have purchased Customs items in your order, a separate notification email will be sent out. ORDER NUMBER: 86989803VIEW ORDER DETAILS Classic Slip-On Checkerboard Stackform Shoe Size: 6.0 Boys = 7.5 Women Color: Marshmallow/Turtledove Quantity: 1 $59.50 This email was sent by: Vans, Inc. 1588 South Coast Drive Costa Mesa, CA, 92626, US 
 
"""

e10="""
These deals are the talk of the Wayborhood!͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­ ͏ ­Shop SaleNew Arrivals Wayfair ProfessionalWayfair Credit CardGift CardsWayfair Exclusive BrandsFamily of BrandsContact Us | My Account This message was sent to erinsalik@gmail.com. To manage your email preferences, click here.If you no longer wish to receive emails from us, click here. To read our privacy policy, click here.Product prices and availability are limited time and subject to change.Quoted prices are in U.S. dollars and are exclusive of shipping and handling or sales taxes, if applicable.Wayfair Inc., 4 Copley Place, Floor 7, Boston, MA 021161Major Purchase Plans*Valid through 05/31/20249.99% APR for 36 months* on orders over $1,5999.99% APR for 48 months* on orders over $1,7999.99% APR for 60 months* on orders over $1,999*With credit approval for qualifying purchases made on the Wayfair Credit Card or Wayfair Mastercard at participating Wayfair sites. Financing not available in all stores. Other financing options are available for qualifying purchases made with the Wayfair Credit Card. Visit Wayfair.com/wayfaircard for details. Additional monthly payments may be required if you have other balances or late payments. See card agreement for details. Promotional financing orders will not earn Rewards and are not eligible for the introductory offer.

"""


print('-------------------------------------------')
print(e1)
print()
print(classify_email(e1))
print('-------------------------------------------')
print(e2)
print()
print(classify_email(e2))
print('-------------------------------------------')
print(e3)
print()
print(classify_email(e3))
print('-------------------------------------------')
print(e4)
print()
print(classify_email(e4))
print('-------------------------------------------')
print(e5)
print()
print(classify_email(e5))
print('-------------------------------------------')
print(e6)
print()
print(classify_email(e6))
print('-------------------------------------------')
print(e7)
print()
print(classify_email(e7))
print('-------------------------------------------')
print(e8)
print()
print(classify_email(e8))
print('-------------------------------------------')
print(e9)
print()
print(classify_email(e9))
print('-------------------------------------------')
print(e10)
print()
print(classify_email(e10))


