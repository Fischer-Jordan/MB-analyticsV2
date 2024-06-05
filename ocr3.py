import requests
import json
from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification

# Step 1: Fetching the Dataset
url = "https://datasets-server.huggingface.co/rows?dataset=Theivaprakasham%2Fwildreceipt&config=WildReceipt&split=train&offset=0&length=100"
response = requests.get(url)
data = response.json()

# Step 2: Parsing the Dataset
rows = data.get("rows", [])
parsed_data = []

for row in rows:
    words = row.get("row", {}).get("words", [])
    image_path = row.get("row", {}).get("image_path", "")
    parsed_data.append({
        "words": " ".join(words),
        "image_path": image_path
    })

# Step 3: Initialize LayoutLM Tokenizer and Model
tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")

# Step 4: Feed Data to the Model
inputs = tokenizer([data['words'] for data in parsed_data], return_tensors="pt", padding=True, truncation=True, max_length=512)

# Assuming you're using the model for classification, here's a placeholder prediction:
with torch.no_grad():
    outputs = model(**inputs)
predictions = outputs.logits.argmax(dim=-1)

# Step 5: Generating Output
output_data = {
    "predictions": predictions.tolist(),
    "image_paths": [data['image_path'] for data in parsed_data]
}

print(json.dumps(output_data, indent=4))
