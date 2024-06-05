

from datetime import datetime
import os
import time
from typing import List
import random
import json

import pickle
import time

import re


from dotenv import load_dotenv
load_dotenv()

import os
import base64
import imaplib
import email
import io
from datetime import datetime, timedelta
import csv



class EmailScraper:
    """A class for scraping emails from Gmail"""

    def __init__(self):
        self.IMAP_SERVER = "imap.gmail.com"
        self.IMAP_PORT = 993
        self.EMAIL = "swathi.mohan@fischerjordan.com"
        self.EMAIL_PASSWORD = "psic nrvd fxzc ctfn"





    def login_and_fetch_email(self):
        try:
            mail = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
            mail.login(self.EMAIL, self.EMAIL_PASSWORD)
            print('logged in')
            mail.select('inbox')
            print('selected inbox')
            # Fetch all emails
            result, data = mail.search(None, 'ALL')
        
            
            email_ids = data[0].split()

            emails = []
            for email_id in email_ids:
                result, data = mail.fetch(email_id, '(RFC822)')
                
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                

                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = msg.get_payload(decode=True).decode('utf-8')

                emails.append({'From': msg['From'], 'Subject': msg['Subject'], 'Date': msg['Date'], 'Body': body})

            # Save emails to a CSV file
            with open('emails.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['From', 'Subject', 'Date', 'Body']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for email in emails:
                    writer.writerow(email)

            print('Emails have been saved to CSV.')
            return len(emails)

        except Exception as e:
            print("An error occurred:", e)
            return 0





#Example usage
if __name__ == "__main__":
    scraper = EmailScraper()
    verification_code = scraper.login_and_fetch_email()
