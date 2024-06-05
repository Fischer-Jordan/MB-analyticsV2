# Import necessary libraries
import torch
from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification
from paddleocr import PaddleOCR
from PIL import Image

# Open the image file
img = Image.open('receipt2.jpg')

# Get the image size
img_width, img_height = img.size

# Initialize the OCR engine and load the LayoutLM model and tokenizer
ocr = PaddleOCR()
model_name = 'microsoft/layoutlm-base-uncased'
model = LayoutLMForTokenClassification.from_pretrained(model_name)
tokenizer = LayoutLMTokenizer.from_pretrained(model_name)

# Apply OCR to the image to detect text and their positions
result = ocr.ocr('receipt2.jpg')

# Function to scale the bounding box coordinates to fit within the 0-1000 range
def scale_bbox(bbox, img_width, img_height):
    scaled_bbox = [
        [
            max(0, min(int(coord / img_width * 1000), 1000)) if idx % 2 == 0 else 
            max(0, min(int(coord / img_height * 1000), 1000)) 
            for idx, coord in enumerate(sub_bbox)
        ] 
        for sub_bbox in bbox
    ]
    
    return scaled_bbox

# Function to convert the OCR output into a format suitable for LayoutLM
def ocr_to_layoutlm(ocr_output, img_width, img_height):
#   print("OCR OUTPUT: ", ocr_output)

  lines = []
  words = []
  for line_info in ocr_output:
      for word_info in line_info:
         # Scale the bounding box coordinates
          scaled_box = scale_bbox(word_info[0], img_width, img_height)
          lines.append(scaled_box)
          words.append(word_info[1][0])
  
  return lines, words

# Use this function to get the bounding boxes and words
lines, words = ocr_to_layoutlm(result, img_width, img_height)
print()
print(lines)
print(words)
inputs = tokenizer(" ".join(words), return_tensors='pt', padding=True, truncation=True)

# Convert the bounding box coordinates to a different format
# Convert the bounding box coordinates to a different format
lines = [[min(coord) for coord in sub_line] + [max(coord) for coord in sub_line] for sub_line in lines]

# Reshape bounding box coordinates to match expected shape [batch_size, num_tokens, 4]
# Assuming there's only one image and len(words) bounding boxes
bbox_tensor = torch.tensor([lines])
print(bbox_tensor)

# Add the bounding box information to the inputs
inputs['bbox'] = bbox_tensor
print("SHAPE: ",bbox_tensor.shape)
# valid_bbox = bbox_tensor[(bbox_tensor[:, :, 2] - bbox_tensor[:, :, 0]).abs() > 1e-5, (bbox_tensor[:, :, 3] - bbox_tensor[:, :, 1]).abs() > 1e-5]

# Run the model
outputs = model(**inputs)

# Get the predicted labels
predicted_labels = torch.argmax(outputs.logits, dim=-1)

# Decode the predicted labels
decoded_labels = tokenizer.convert_ids_to_labels(predicted_labels)

print(decoded_labels)
