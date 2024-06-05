

from openai import OpenAI
import json
import requests 
import os
import csv

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)

brands = ['nike', 'adidas', 'puma']
items = ['shoes', 't-shirts', 'pants']
vendors = ['Amazon', 'Walmart', 'Target']
captions = ['Just bought some new Nike shoes!', 'Love my Adidas t-shirts.', 'Got a great deal on Puma pants at Walmart.']
captions2=['My fav shoes, these are so comfy!', 'Ew Amazon sucks these tshirts are trash bruh do NOT BUY', 'Puma hits different man, pumaforeverrrrrrrrrrrr']
new_item='Laptop'
new_brand='Apple'
new_vendor='Best Buy'


        

def get_json_from_text(brands, items, vendors, captions, new_item, new_brand, new_vendor):
    messages = [{
        "role": "user",
        "content": f"Brands, vendors, items that he purchased and his captions are given by: {brands} {items} {vendors} {captions} . The new brand\
            new vendor and new item for which the new caption should be generated is given by {new_brand} {new_vendor} {new_item}"
    }]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "answer_questions",
                "description": "Given lists above, tell me what kind of caption the user is most likely to write next",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "next_caption": {
                            "type": "string",
                            "description": "The next caption the user might write. Use the existing captions to understand what the user usually writes. Make \
                            sure that the new generated caption is completely different from the existing captions for the new item that user has purchased.\
                            Make sure that the caption only has the new item, new brand and new vendor. Also analyse the language, slang, accent, gen Z attitude\
                            used in the captions and generate appropriately",
                            "enum": captions
                        }
                    },
                    "required": ["next_caption"]
                }
            }
        }
    ]
    try: 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
        )
    except Exception as e:
        raise Exception("OpenAI API error. Please try again later.")
    
    # Step 2: check if GPT wanted to call a function
    if response.choices[0].message.tool_calls[0].function:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

    return None



if __name__ == "__main__": 
    print(get_json_from_text(brands, items, vendors, captions, new_item, new_brand, new_vendor))

      

   