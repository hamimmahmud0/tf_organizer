import keras_ocr

def extract_text_from_image(image_path):
    # Create a Keras-OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()
    
    # Read the image
    image = keras_ocr.tools.read(image_path)
    
    # Recognize text in the image
    predictions = pipeline.recognize([image])
    
    # Extract text from predictions
    texts = [text for (_, text) in predictions[0]]
    
    # Combine texts into a single string
    combined_text = ' '.join(texts)
    
    return combined_text


if __name__ == "__main__":
    input_image = 'image.png'
    extracted_text = extract_text_from_image(input_image)
    print("Extracted Text:")
    print(extracted_text)