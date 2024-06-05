def find_matching_keywords(email, keywords):
    email_lower = email.lower()
    matching_keywords = [keyword for keyword in keywords if keyword.lower() in email_lower]
    return matching_keywords

# Example usage
email = """
ORIGINAL FOR RECIPIENT
Tax Invoice
ZOMATO LIMITED (FORMERLY KNOWN AS ZOMATO PRIVATE LIMITED AND ZOMATO
MEDIA PRIVATE LIMITED)
Address: Pioneer Square, Tower 1-
Ground to 6th Floor and Tower
2- 1st and 2nd Floors, Near
Golf Course Extension,
sector-62, Gurugram,
Gurugram, Haryana, 122098PAN: AADCD4946L
State: Haryana CIN: L93030DL2010PLC198141
Email ID: order@zomato.com GSTIN: 06AADCD4946L1ZE
Invoice No: Z24HROT000377506 Invoice Date: 2024-01-30
Customer Details
Name: Param Kapur GSTIN: UNREGISTERED
Address: 14B Venetia Tower, 122102 Place of Supply: Haryana(6)
Service Details
HSN Code: 999799 Supply Description: Other Services N.E.C
Sr.No Particulars Taxable Amount CGST SGST Total
Order ID :5538219099
Order Date :2024-01-30
1 Platform fee 3.00 0.27 0.27 3.54
Total 3.00 0.27 0.27 3.54
Amount ₹3.54 settled through digital mode through multiple transactions net payout settlement via reference id 5538219099 dated (2024-01-30)
(19:45)'
Tax is not payable on reverse charge basis
For Zomato Limited (Formerly known as Zomato Private Limited and Zomato Media Private Limited)
Authorised Signatory
Communication Address: Pioneer Square, Tower 1- Ground to 6th Floor and Tower 2- 1st and 2nd Floors, Near Golf Course Extension,
sector-62, Gurugram, Gurugram, Haryana, 122098
Please refer to https://www.zomato.com/conditions for current version of full terms & conditions which are incorporated in this invoice by reference.
Powered by TCPDF (www.tcpdf.org)
"""

invoice_indicative_keywords = [
    'invoice #', 'order number', 'order #', 'invoice', 'purchase', 'HSN Code', 'Bill to', 'Total invoice value', 'Ship to', 'Address', 'Tax invoice', 'Order ID'
]

matching_keywords = find_matching_keywords(email, invoice_indicative_keywords)
print("Matching keywords:", matching_keywords)
