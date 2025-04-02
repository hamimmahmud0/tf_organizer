import keras_ocr, json
import matplotlib.pyplot as plt
import numpy as np

def extract_text_from_image(image_path):
    # Create a Keras-OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()
    
    # Read the image
    images = [keras_ocr.tools.read(image_path)]
    
    # Recognize text in the image
    prediction_groups = pipeline.recognize(images)
    
    boxes = [arr[1] for arr in prediction_groups[0]]
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
        "text": [arr[0] for arr in prediction_groups[0]],
    }
    with open('block/{name}.json'.format(name = image_path.split('.')[0].split('/')[1]), 'w') as f:
        json.dump(block_image_info, f, indent=2)

    fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    for ax, image, predictions in zip([axs], images, prediction_groups):
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
    plt.savefig('ocr/{name}.png'.format(name=image_path.split('.')[0].split('/')[1]))


if __name__ == "__main__":
    for x in range(20):
        extract_text_from_image('img/{}.png'.format(x+1))