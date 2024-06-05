from transformers import XLNetTokenizer, XLNetLMHeadModel
import torch

# Dummy data
brands = ['nike', 'adidas', 'puma']
items = ['shoes', 't-shirts', 'pants']
vendors = ['Amazon', 'Walmart', 'Target']
captions = ['Just bought some new Nike shoes!', 'Love my Adidas t-shirts.', 'Got a great deal on Puma pants at Walmart.']

# Combine all data into a single list
data = brands + items + vendors + captions

# Initialize XLNet tokenizer and model
tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
model = XLNetLMHeadModel.from_pretrained('xlnet-base-cased')

# Tokenize input data
input_ids = tokenizer.encode(" ".join(data), return_tensors="pt")

# Generate output using XLNet model
output = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95, temperature=0.7)

# Decode and print the generated caption
generated_caption = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Caption:", generated_caption)
