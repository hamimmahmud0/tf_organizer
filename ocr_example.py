import keras_ocr

def extract_text_from_image(image_path):
    # Create a Keras-OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()
    
    # Read the image
    image = keras_ocr.tools.read(image_path)
    
    # Recognize text in the image
    predictions = pipeline.recognize([image])
    
    for text, bounding_box in predictions[0]:
        print(text)


if __name__ == "__main__":
    input_image = 'image.png'
    extract_text_from_image(input_image)