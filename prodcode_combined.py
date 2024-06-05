import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import os
sub1="Fwd: Swissôtel Hotels Reservation Details: 09-Jul-2024"
 

sub2="Summer is calling 📞 $25 off SITEWIDE + free gift"


sub3="""
Fwd: [Personal] Your Sunday afternoon trip with Uber
"""


sub4="	Order Confirmation - Paleovalley.com"


sub5="Your transfer's complete"


sub6="Summer 2024: Launching Soon 👀"


sub7="Your Amazon.com order of Logical Chess, Move by Move has shipped!"


sub8="New Arrivals: Sandals with ornate detailing"


sub9="Your order is almost ready to ship"


sub10="""
Justworks invoice for $883.05 will be debited on 05/21/202
"""

sub11="""
Successful Transaction for Order #4318 - Holland Group
"""

e1="""
Another one.Anthony Mavromatisahm203@yahoo.com(347) 661-8316> Begin forwarded message:> > From: > Subject: Swissôtel Hotels Reservation Details: 09-Jul-2024> Date: May 30, 2024 at 10:55:36 AM EDT> To: > > Please do not respond to this email. Inquiries should be directed to the specific hotel or please call 1 888 540 6066> > RESERVATION> > > > DEAR MR ANTHONY MAVROMATIS> Thank you for booking online, your reservation was completed successfully.> Your reservation number is: > 231983519 > > Please refer to the reservation details below and visit our hotel links for more information to plan your visit. > > Below are your reservation details. If you have any questions please call 1 888 737 9477 > ARRIVING on 09-Jul-2024> DEPARTING on 10-Jul-2024> TOTAL NIGHTS: 1> NUMBER OF GUESTS:2 Adult , 0 Children > ROOM RATE: $305 USD> ROOM TYPE: Classic Riverview 1 King> PROMOTIONAL CODE: None> FAMOUS AGENT: > MEMBER NUMBER: 3081031485333711> ROOM RATE DESCRIPTION: Fully Flexible - Best available rate> IATA CODE: > EXTRAS:> TOTALS:> Room: $381.56 USD> Extras: $0 USD> TOTAL RATE: $381.56 USD> > DEPOSIT POLICY: NO DPST IS REQUIRED> CANCEL POLICY: CXL BY 07/07/24 4PM> CANCEL BY: CXL BY 07/07/24 4PM> > > > ANTHONY MAVROMATIS- You are Eligible for a Custom Upgrade> Elevate your experience with premium upgrade opportunities, starting at $42 per night!> > SHOW MY CUSTOM UPGRADE> > > SWISSOTEL CHICAGO> 323 East Upper Wacker Drive, Chicago > United States> Tel: ++1 312 565 0565 > Fax: ++1 312 268 8252> E-mail: chicago@swissotel.com > For more information on Swissotel Chicago click here > QUICK LINKS> > Hotel Fact Sheet > Find out about the ALL loyalty programme > Sign in to your ALL account > Cancel/Modify Reservation > Swissotel Reservations - 1 888 540 6066 - Click here for additional telephone numbers> Click here to view our Privacy Policy.> Last Updated: 29/11/2019 Swissotel Hotels & Resorts © 2019> This e-mail, any attachments and the information contained therein ("this message") are confidential and intended solely for the use of the addressee(s). If you have received this message in error please send it back to the sender and delete it. Unauthorized publication, use, dissemination or disclosure of this message, either in whole or in part is strictly prohibited.> > Ce message electronique ainsi que tous les fichiers joints et les informations contenus dans ce message (ci apres "le message"), sont confidentiels et destines exclusivement a l'usage de la personne a laquelle ils sont adresses. Si vous avez recu ce message par erreur, merci de le renvoyer a son emetteur et de le detruire. Toute diffusion, publication, totale ou partielle ou divulgation sous quelque forme que ce soit non expressement autorisees de ce message, sont interdites.> Another one.Anthony Mavromatisahm203@yahoo.com(347) 661-8316Begin forwarded message:From: <SCH.reservations@swissotel.com>Subject: Swissôtel Hotels Reservation Details: 09-Jul-2024Date: May 30, 2024 at 10:55:36 AM EDTTo: <ahm203@yahoo.com>Please do not respond to this email. Inquiries should be directed to the specific hotel or please call 1 888 540 6066RESERVATIONDEAR MR ANTHONY MAVROMATISThank you for booking online, your reservation was completed successfully.Your reservation number is: 231983519 Please refer to the reservation details below and visit our hotel links for more information to plan your visit. Below are your reservation details. If you have any questions please call 1 888 737 9477 ARRIVING on 09-Jul-2024DEPARTING on 10-Jul-2024TOTAL NIGHTS: 1NUMBER OF GUESTS:2 Adult , 0 Children ROOM RATE: $305 USDROOM TYPE: Classic Riverview 1 KingPROMOTIONAL CODE: NoneFAMOUS AGENT: MEMBER NUMBER: 3081031485333711ROOM RATE DESCRIPTION: Fully Flexible - Best available rateIATA CODE: EXTRAS:TOTALS:Room: $381.56 USDExtras: $0 USDTOTAL RATE: $381.56 USDDEPOSIT POLICY: NO DPST IS REQUIREDCANCEL POLICY: CXL BY 07/07/24 4PMCANCEL BY: CXL BY 07/07/24 4PM ANTHONY MAVROMATIS- You are Eligible for a Custom UpgradeElevate your experience with premium upgrade opportunities, starting at $42 per night!SHOW MY CUSTOM UPGRADE SWISSOTEL CHICAGO323 East Upper Wacker Drive, Chicago United StatesTel: ++1 312 565 0565 Fax: ++1 312 268 8252E-mail: chicago@swissotel.comFor more information on Swissotel Chicago click hereQUICK LINKSHotel Fact SheetFind out about the ALL loyalty programmeSign in to your ALL accountCancel/Modify ReservationSwissotel Reservations - 1 888 540 6066 - Click here for additional telephone numbersClick here to view our Privacy Policy.Last Updated: 29/11/2019 Swissotel Hotels & Resorts © 2019This e-mail, any attachments and the information contained therein ("this message") are confidential and intended solely for the use of the addressee(s). If you have received this message in error please send it back to the sender and delete it. Unauthorized publication, use, dissemination or disclosure of this message, either in whole or in part is strictly prohibited.Ce message electronique ainsi que tous les fichiers joints et les informations contenus dans ce message (ci apres "le message"), sont confidentiels et destines exclusivement a l'usage de la personne a laquelle ils sont adresses. Si vous avez recu ce message par erreur, merci de le renvoyer a son emetteur et de le detruire. Toute diffusion, publication, totale ou partielle ou divulgation sous quelque forme que ce soit non expressement autorisees de ce message, sont interdites.
 
"""

e2="""
Lift, hydrate + tone skin from head-to-toe 💪 | [View in Browser](https://manage.kmail-lists.com/subscriptions/web-view?a=XF5dmK&c=01G919VHE92S2YMC40KKKXEY20&k=c1a1564ede77b77d05289e6f0f567d79&m=01HYE6459TH2F9H5WWBGBW35TD&r=3795PNHx)[Biossance.](https://biossance.com/)[Shop](https://biossance.com/collections/all)[Bestsellers](https://biossance.com/collections/bestsellers)[NEW](https://biossance.com/collections/new)[Free Fresh-Faced Trio on Orders $75+](https://www.biossance.com/c/offers/memorial-day-sale/?position=tb)[Memorial Day Sale $25 Off $75+ Sitewide](https://www.biossance.com/c/offers/memorial-day-sale/?position=hero)[Memorial Day Sale $25 Off $75+ Sitewide](https://www.biossance.com/c/offers/memorial-day-sale/?position=sm)[BIOSSANCE BENEFITS](https://biossance.com/collections/all)[Free shipping.](https://biossance.com/collections/all) [FREE SHIPPING](https://biossance.com/collections/all)[on U.S. orders $50+](https://biossance.com/collections/all)[Easy returns.](https://biossance.com/a/returns) [EASY & FREE RETURNS](https://www.biossance.com/c/returns/)[for up to 30 days](https://biossance.com/a/returns)[Clean Crew benefits.](https://biossance.com/pages/clean-crew-loyalty-rewards)https://www.biossance.com/c/loyalty-program/ [our free rewards program](https://biossance.com/pages/clean-crew-loyalty-rewards)[Trust Icons.](https://biossance.com/pages/sustainability)[Instagram.](https://www.instagram.com/biossance/)[TikTok.](https://www.tiktok.com/@biossance)[Facebook.](https://www.facebook.com/biossance)[YouTube.](https://www.youtube.com/channel/UCP9OYSjsvKCxJU5ydrGuTlw)[Biossance Blog.](https://biossance.com/blogs/lab-notes)Receive $25 off $75+ purchases, discount automatically applied at checkout. Valid until 05/27/2024 11:59PM PT. $75 minimum purchase before tax must be met before discount can be applied. One discount per qualified purchase. Offer only valid on merchandise purchases made on Biossance.com . Not valid on previous purchases, e-gift cards, travel sizes, bundles, taxes, or shipping & handling charges. Return of discounted merchandise will be for price actually paid. Offer has no cash value and may not be altered, sold, bartered or transferred. Cannot be used in conjunction with other offer, promo codes, or reward. Biossance may modify or cancel offer at any time and reserves the right, with or without notice, to cancel or limit the sale of our products. Receive the free 3-pc gift, while supplies last or by 5/27/2024 at 11:59PM PT, with $75+ merchandise purchase on Biossance.com . Gift Includes Travel Size Rose Vegan Lip Balm, Travel Size Hyaluronic Toning Mist, and Deluxe Size Probiotic Gel Moisturizer. No code needed. Sales tax, shipping & handling, gift cards, or previous purchases do not qualify towards minimum purchase amount. Minimum must be met before taxes and after discounts are applied. Offer is nontransferable. Not valid on previous purchases, purchases of gift cards, taxes, or shipping & handling charges. Offer not available at Sephora. Offer has no cash value and is void if altered, sold, bartered, or transferred. Cannot be used in conjunction with other codes. Biossance may modify or cancel offer(s) at any time and reserves the right, with or without notice, to cancel or limit the sale of our products. *Free shipping on US domestic orders $50+ on biossance.com for a limited time. Minimum must be met before taxes and after discounts are applied. No code needed. Offer not valid on previously purchased merchandise, gift-cards, or sales tax. Price match not available on previously placed orders. Biossance reserves the right to extend, modify, eliminate, or reduce this promotion at any time. Offer has no cash value and may not be altered, sold, bartered or transferred. Please do not reply to this email.* Orders processed and shipped Monday through Friday, excluding holidays. All orders placed by 9 am PST (Monday – Friday) will be processed same day. For questions about an order, other questions or comments, contact [Customer Service](https://www.biossance.com/c/help-centre/).[Unsubscribe](https://manage.kmail-lists.com/subscriptions/unsubscribe?a=XF5dmK&c=01G919VHE92S2YMC40KKKXEY20&k=c1a1564ede77b77d05289e6f0f567d79&m=01HYE6459TH2F9H5WWBGBW35TD&r=3795PNHx) | [Manage Preferences](https://manage.kmail-lists.com/subscriptions/update?a=XF5dmK&c=01G919VHE92S2YMC40KKKXEY20&k=c1a1564ede77b77d05289e6f0f567d79&m=01HYE6459TH2F9H5WWBGBW35TD&r=3795PNHx) | [Privacy Policy](https://www.biossance.com/c/privacy-policy/) | [Contact Us](https://www.biossance.com/c/help-centre/)This email was sent by: 2024 © Biossance.Registered office: 5th Floor 115 Broadway, 115 Broadway Street, New York, NY 10006 Lift, hydrate + tone skin from head-to-toe 💪 ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ ­ Lift, hydrate + tone skin from head-to-toe 💪 | View in BrowserShopBestsellersNEW BIOSSANCE BENEFITS FREE SHIPPINGon U.S. orders $50+ EASY & FREE RETURNSfor up to 30 days our free rewards program Receive $25 off $75+ purchases, discount automatically applied at checkout. Valid until 05/27/2024 11:59PM PT. $75 minimum purchase before tax must be met before discount can be applied. One discount per qualified purchase. Offer only valid on merchandise purchases made on Biossance.com . Not valid on previous purchases, e-gift cards, travel sizes, bundles, taxes, or shipping & handling charges. Return of discounted merchandise will be for price actually paid. Offer has no cash value and may not be altered, sold, bartered or transferred. Cannot be used in conjunction with other offer, promo codes, or reward. Biossance may modify or cancel offer at any time and reserves the right, with or without notice, to cancel or limit the sale of our products. Receive the free 3-pc gift, while supplies last or by 5/27/2024 at 11:59PM PT, with $75+ merchandise purchase on Biossance.com . Gift Includes Travel Size Rose Vegan Lip Balm, Travel Size Hyaluronic Toning Mist, and Deluxe Size Probiotic Gel Moisturizer. No code needed. Sales tax, shipping & handling, gift cards, or previous purchases do not qualify towards minimum purchase amount. Minimum must be met before taxes and after discounts are applied. Offer is nontransferable. Not valid on previous purchases, purchases of gift cards, taxes, or shipping & handling charges. Offer not available at Sephora. Offer has no cash value and is void if altered, sold, bartered, or transferred. Cannot be used in conjunction with other codes. Biossance may modify or cancel offer(s) at any time and reserves the right, with or without notice, to cancel or limit the sale of our products. *Free shipping on US domestic orders $50+ on biossance.com for a limited time. Minimum must be met before taxes and after discounts are applied. No code needed. Offer not valid on previously purchased merchandise, gift-cards, or sales tax. Price match not available on previously placed orders. Biossance reserves the right to extend, modify, eliminate, or reduce this promotion at any time. Offer has no cash value and may not be altered, sold, bartered or transferred. Please do not reply to this email.* Orders processed and shipped Monday through Friday, excluding holidays. All orders placed by 9 am PST (Monday – Friday) will be processed same day. For questions about an order, other questions or comments, contact Customer Service.Unsubscribe | Manage Preferences | Privacy Policy | Contact Us This email was sent by: 2024 © Biossance.Registered office: 5th Floor 115 Broadway, 115 Broadway Street, New York, NY 10006

"""
e3="""
Reebok Going going… VIEW IN BROWSERPrices are marked. Valid thru 5/5. Exclusions apply. Shop Now FREE SHIPPING ON ORDERS OF $75 OR MOREMY ACCOUNTFIND A STORENEED HELP?Free ground shipping offer on orders of $75 or more valid to U.S. addresses only. All offers valid on domestic U.S. orders only.This email was sent to: erinsalik@gmail.comUnsubscribe and Manage My Preferences | Contact Us | Privacy Policy This email was sent by: Reebok International Ltd., LLC | 25 Drydock Ave. | Boston, MA 02210 | United States © 2024 Reebok. All Rights Reserved. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
 
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
--- --- --- --- --- --- --- ---JustworksFischer Jordan LLC--- --- --- --- --- --- --- ---Hi Boaz,Your Justworks invoice for $883.05 is being debited from your bank account ending in XXXX8140. Here are the details: Invoice ID: 7F36AEB6-E016-4EC2-8A95-526C5CFE25FF Amount Due: $883.05 Debit Date: 05/21/2024 Payment: Direct debit from XXXX8140You can view the full details of this invoice, including a detailed breakdown of all earnings, taxes and fees, by signing into Justworks and clicking on Payments > Invoices.Please ensure that sufficient funds are present in your account to cover this debit. As always, please don’t hesitate to reach out if you have any questions. You can reach us at 1‑888‑534‑1711 or support@justworks.comThanks,The Justworks Team--- --- --- --- --- --- --- ---This email was sent as a result of an action that you or someone in your organization took. Add support@justworks.com to your address book to ensure delivery to your inbox.Justworks, Inc. and its affiliates. 55 Water St, 29th Floor, New York, NY 10041--- --- --- --- --- --- --- ---Justworks Fischer Jordan LLC Justworks invoice for $883.05 will be debited on 05/21/2024Hi Boaz, Your Justworks invoice for $883.05 is being debited from your bank account ending in XXXX8140.Invoice ID7F36AEB6-E016-4EC2-8A95-526C5CFE25FFAmount Due $883.05 Debit Date 05/21/2024 Payment Direct debit from XXXX8140 You can view the full details of this invoice, including a detailed breakdown of all earnings, taxes and fees, by signing into Justworks and clicking on Payments > Invoices. Please ensure that sufficient funds are present in your account to cover this debit. As always, please don’t hesitate to reach out if you have any questions. You can reach us at 1‑888‑534‑1711 or support@justworks.comThanks,The Justworks Team This email was sent as a result of an action that you or someone in your organization took. Add support@justworks.com to your address book to ensure delivery to your inbox. Justworks, Inc. and its affiliates. 55 Water St, 29th Floor, New York, NY 10041

"""
e11="""
Hey Anthony and Boaz,We’ve debugged the issue with the email classifier (as explained below).This was an oversight on our part after we made improvements to the emailinbox fetching. This issue will not occur again.Best,Param Param Kapur FischerJordan+91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If youare not an intended recipient of this email, please immediately notify thesender by replying to this email, delete the message and any attachmentsfrom your account, and do not forward or otherwise distribute the messageor any attachments.---------- Forwarded message ---------From: Swathi Mohan Date: Thu, May 16, 2024 at 00:07Subject: Regarding classifierTo: Param Kapur Hey Param,The classifier is working fine now. The issue was that, in thebackend, we were classifying the html content of the email, instead ofthe actual email text. So all the emails were getting classified asspam. I've fixed it and now you'll be able to see the invoices againRegardsSwathi MohanHey Anthony and Boaz, We’ve debugged the issue with the email classifier (as explained below). This was an oversight on our part after we made improvements to the email inbox fetching. This issue will not occur again. Best,Param Param Kapur FischerJordan +91 9871587593 param.kapur@fischerjordan.com This e-mail message is intended only for the named recipients above. If you are not an intended recipient of this email, please immediately notify the sender by replying to this email, delete the message and any attachments from your account, and do not forward or otherwise distribute the message or any attachments.---------- Forwarded message ---------From: Swathi Mohan <swathi.mohan@fischerjordan.com>Date: Thu, May 16, 2024 at 00:07Subject: Regarding classifierTo: Param Kapur <param.kapur@fischerjordan.com>Hey Param,The classifier is working fine now. The issue was that, in thebackend, we were classifying the html content of the email, instead ofthe actual email text. So all the emails were getting classified asspam. I've fixed it and now you'll be able to see the invoices againRegardsSwathi Mohan

"""

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
        return prediction_email
    else:
        if prediction_subject == 'invoice' and prediction_email == 'spam':
            if invoice_confidence_subject > spam_confidence_email:
                return 'invoice'
            else:
                return 'spam'
        elif prediction_subject == 'spam' and prediction_email == 'invoice':
            if spam_confidence_subject > invoice_confidence_email:
                return 'spam'
            else:
                return 'invoice'
      

print('-------------------------------------------')
print('SUBJECT: ', sub1)
print()
print(classify_subject(sub1))
print()
print('EMAIL: ',e1)
print()
print(classify_email(e1))
print('FINAL DECISION: ', decide(e1,sub1))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub2)
# print()
# print(classify_subject(sub2))
# print()
# print('EMAIL: ',e2)
# print()
# print(classify_email(e2))
# print('FINAL DECISION: ', decide(e2,sub2))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub3)
# print()
# print(classify_subject(sub3))
# print()
# print('EMAIL: ',e3)
# print()
# print(classify_email(e3))
# print('FINAL DECISION: ', decide(e3,sub3))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub4)
# print()
# print(classify_subject(sub4))
# print()
# print('EMAIL: ',e4)
# print()
# print(classify_email(e4))
# print('FINAL DECISION: ', decide(e4,sub4))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub5)
# print()
# print(classify_subject(sub5))
# print()
# print('EMAIL: ',e5)
# print()
# print(classify_email(e5))
# print('FINAL DECISION: ', decide(e5,sub5))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub6)
# print()
# print(classify_subject(sub6))
# print()
# print('EMAIL: ',e6)
# print()
# print(classify_email(e6))
# print('FINAL DECISION: ', decide(e6,sub6))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub7)
# print()
# print(classify_subject(sub7))
# print()
# print('EMAIL: ',e7)
# print()
# print(classify_email(e7))
# print('FINAL DECISION: ', decide(e7,sub7))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub8)
# print()
# print(classify_subject(sub8))
# print()
# print('EMAIL: ',e8)
# print()
# print(classify_email(e8))
# print('FINAL DECISION: ', decide(e8,sub8))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub9)
# print()
# print(classify_subject(sub9))
# print()
# print('EMAIL: ',e9)
# print()
# print(classify_email(e9))
# print('FINAL DECISION: ', decide(e9,sub9))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub10)
# print()
# print(classify_subject(sub10))
# print()
# print('EMAIL: ',e10)
# print()
# print(classify_email(e10))
# print('FINAL DECISION: ', decide(e10,sub10))

# print('-------------------------------------------')
# print('-------------------------------------------')
# print('SUBJECT: ', sub11)
# print()
# print(classify_subject(sub11))
# print()
# print('EMAIL: ',e11)
# print()
# print(classify_email(e11))
# print('FINAL DECISION: ', decide(e11,sub11))