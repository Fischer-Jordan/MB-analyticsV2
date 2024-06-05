# import easyocr

# def extract_text(image_path):
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_path)
#     text_list = []
#     for (bbox, text, prob) in results:
#         # bbox is the bounding box around the text
#         # text is the extracted text
#         # prob is the probability of the recognized text
#         print(f"Detected text: {text} (Confidence: {prob:.2f})")
#         text_list.append(text)

#     return text_list

# # Replace 'path/to/receipt.jpg' with the path to your receipt image
# image_path = 'receipt3.png'
# extracted_text = extract_text(image_path)
# combined_text = ' '.join(extracted_text)

# print("\nCombined Extracted Text:")
# print(combined_text)



# # ------------------------------------------------------------------------------------------------



# import pytesseract
# from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Swathi\\OCR\\tesseract.exe'

# def extract_text_from_image(image_path):
#     """
#     This function takes the path of an image as input,
#     extracts text from the image using Tesseract OCR,
#     and returns the text as a string.
#     """
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)
#         return text
#     except Exception as e:
#         return str(e)

# def save_text_to_file(text, file_path):
#     """
#     This function takes a text string and a file path as input
#     and writes the text to the file.
#     """
#     try:
#         with open(file_path, 'w') as file:
#             file.write(text)
#         return True
#     except Exception as e:
#         print(f"Error writing to file: {e}")
#         return False

# image_path = 'receipt1.png'
# extracted_text = extract_text_from_image(image_path)
# text_file_path = 'receipt1.txt'

# if save_text_to_file(extracted_text, text_file_path):
#     print(f"Text successfully written to {text_file_path}")
# else:
#     print(f"Failed to write text to {text_file_path}")




# ------------------------------------------------------------------------------------------------





import json
import requests
url="https://ocr.asprise.com/api/v1/receipt"
image="receipt3.png"
res=requests.post(url,
                  data={
                      'api_key':'TEST',
                      'recognizer':'auto',
                      'ref_no':'oct_python_123',
                  },
                  files={
                      'file':open(image, 'rb')
                  })


data=json.loads(res.text)
print(data)

def convert_to_text(data):
    text_output = ""
    if data.get("success") and "receipts" in data:
        for receipt in data["receipts"]:
            text_output += "Receipt Details:\n"
            text_output += "------------------------------\n"
            text_output += f"Merchant Name: {receipt.get('merchant_name', 'N/A')}\n"
            text_output += f"Phone: {receipt.get('merchant_phone', 'N/A')}\n"
            text_output += f"Merchant Address: {receipt.get('merchant_address', 'N/A')}\n"
            text_output += f"Merchant Email: {receipt.get('merchant_email', 'N/A')}\n"  # if available
            text_output += f"Date: {receipt.get('date', 'N/A')} Time: {receipt.get('time', 'N/A')}\n"
            text_output += f"Total: {receipt.get('total', 'N/A')} {receipt.get('currency', '')}\n"
            text_output += "Items Purchased:\n"
            for item in receipt.get("items", []):
                description = item.get("description", "N/A")
                amount = item.get("amount", "N/A")
                text_output += f" - {description}: {amount}\n"
            text_output += "\nAdditional Info:\n"
            text_output += f"Tax: {receipt.get('tax', 'N/A')}\n"
            text_output += f"Subtotal: {receipt.get('subtotal', 'N/A')}\n"
            text_output += f"Receipt No: {receipt.get('receipt_no', 'N/A')}\n"
            
            # Additional details
            text_output += f"Payee Name: {receipt.get('payee_name', 'N/A')}\n"
            text_output += f"Payee Address: {receipt.get('payee_address', 'N/A')}\n"
            text_output += f"Payee Phone: {receipt.get('payee_phone', 'N/A')}\n"
            text_output += f"Payee Email: {receipt.get('payee_email', 'N/A')}\n"
            text_output += f"Vendor Address: {receipt.get('vendor_address', 'N/A')}\n"
            text_output += f"Vendor Email: {receipt.get('vendor_email', 'N/A')}\n"
            text_output += f"Brand Address: {receipt.get('brand_address', 'N/A')}\n"
            text_output += f"Brand Email: {receipt.get('brand_email', 'N/A')}\n"
            text_output += f"Brand Website: {receipt.get('brand_website', 'N/A')}\n"
            
            text_output += "------------------------------\n\n"

    return text_output

# Convert the JSON data to text
text_data = convert_to_text(data)

# Write the text data to a file named receipt.txt
with open("receipt3.txt", "w") as text_file:
    text_file.write(text_data)

print(f"Receipt data has been written to {text_file}")