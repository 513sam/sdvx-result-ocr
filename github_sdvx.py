import os
import io
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image
import re
# Google Vision Service key
key_path = 'Key_Path'
credentials = service_account.Credentials.from_service_account_file(key_path)

# Google Cloud Vision API Client credentials
client = vision.ImageAnnotatorClient(credentials=credentials)

# Image Path
image_pa = 'Image_Path'
input_image_path = image_pa
output_image_path = 'Resized_Image_Path'
image_paths = ['Resized_Image_Path']
# Resized Image Resolutions
new_width = 1500
new_height = 2000

def resize_image(input_path, output_path, width, height):
    with Image.open(input_path) as img:
        # Resizing Image
        resized_img = img.resize((width, height), Image.LANCZOS)
        # Save resized Image
        resized_img.save(output_path)

# Call resize_image function to resize
resize_image(input_image_path, output_image_path, new_width, new_height)
print(f'Resized image saved to {output_image_path}')

# create box for ocr
def crop_image(image_path, box):
    with Image.open(image_path) as im:
        cropped_image = im.crop(box)
        return cropped_image

# OCR for specific coordinate 
def extract_text_from_box(client, image_path, box):
    cropped_image = crop_image(image_path, box)
    content = io.BytesIO()
    cropped_image.save(content, format='JPEG')
    image = vision.Image(content=content.getvalue())
    response = client.text_detection(image=image)
    if response.text_annotations:
        return response.text_annotations[0].description.strip()
    return "Not found"

# Difficulty and Score boxex
coordinates = {
    'image_path1': {
        'difficulty_box': (268, 908, 508, 1016),
        'score_box': (680, 1128, 1020, 1228),
        'song_box': (568,1056,990,1160)
    }
    ,
    'image_path2': {
        'difficulty_box': (112,884,348,988),
        'score_box': (574,1086,1010,1146),
        'song_box': (502,1022,1026,1098)
    }
}


# OCR
def extract_numbers(text):
    return ''.join(re.findall(r'\d+', text))

# Apply for each pic
for image_path in image_paths:
    difficulty_box = coordinates[image_path]['difficulty_box']
    score_box = coordinates[image_path]['score_box']
    song_box = coordinates[image_path]['song_box']
    
    
    difficulty_text = extract_text_from_box(client, image_path, difficulty_box)
    score_text = extract_text_from_box(client, image_path, score_box)
    song_text = extract_text_from_box(client, image_path, song_box)
    
    score_numbers = extract_numbers(score_text)
    
    print(f'Image: {image_path}')
    print(f'Difficulty: {difficulty_text}')
    print(f'Score: {score_numbers}')
    print(f'Song : {song_text}')
