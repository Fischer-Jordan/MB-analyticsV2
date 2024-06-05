from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw, ImageFont
import csv

ocr = PaddleOCR(lang='en') 
img_path = 'receipt8.png'
result = ocr.ocr(img_path, cls=False)


# with open('sheet3.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for entry in result:
#             for item in entry:
#                 csv_row = []
#                 # Extracting coordinates and text
#                 for coord in item[0]:
#                     csv_row.extend(coord)
#                 text = item[1][0]  # Extracting text from the tuple
#                 csv_row.append(text)
#                 writer.writerow(csv_row)
# print(result)
for line in result:
        boxes = [item[0] for item in line]
        txts = [item[1][0] for item in line]
        scores = [item[1][1] for item in line]


print("\nboxes: ",boxes)
print("\ntexts: ",txts)
with open('boxes.txt', 'w') as boxes_file:
    for box in boxes:
        boxes_file.write(f"{box}\n")

# Write texts to a text file
with open('texts.txt', 'w') as texts_file:
    for text in txts:
        texts_file.write(f"{text}\n")
# print("\nscores: ",scores)



image = Image.open(img_path).convert('RGB')
im_show = draw_ocr(image, boxes, txts, scores, font_path='AovelSansRounded-rdDL.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result4.jpg')
