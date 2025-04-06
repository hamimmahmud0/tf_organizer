import keras_ocr, json
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_text_from_image(image_paths):
    # Create a Keras-OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()
    
    # Read the image
    images = []
    for x in image_paths:
        images.append(keras_ocr.tools.read(x))
    
    # Recognize text in the image
    prediction_groups = pipeline.recognize(images)
    i=0
    for prediction_group in prediction_groups:
            
        image_path = image_paths[i]
        boxes = [arr[1] for arr in prediction_group]
        box_json = []

        for x in boxes:
            box_json.append({
                "x1": float(x[0][0]),
                "y1": float(x[0][1]),
                "x2": float(x[1][0]),
                "y2": float(x[1][1]),
                "x3": float(x[2][0]),
                "y3": float(x[2][1]),
                "x4": float(x[3][0]),
                "y4": float(x[3][1]),   
            })
        block_image_info = {
            "image_shape":[images[0].shape[0], images[0].shape[1]],
            "boxes": box_json,
            "name": image_path,
            "text": [arr[0] for arr in prediction_group],
        }
        with open('block/{name}.json'.format(name = image_path.split('.')[0].split('/')[1]), 'w') as f:
            json.dump(block_image_info, f, indent=2)

        fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
        for ax, image, predictions in zip([axs], images, [prediction_group]):
            keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
        plt.savefig('ocr/{name}.png'.format(name=image_path.split('.')[0].split('/')[1]))

def get_image_files():
    image_dir = 'scraping/pdf_images'
    return [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]

if __name__ == "__main__":
    extract_text_from_image(get_image_files())