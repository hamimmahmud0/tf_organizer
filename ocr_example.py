import keras_ocr
import matplotlib.pyplot as plt

def extract_text_from_image(image_path):
    # Create a Keras-OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()
    
    # Read the image
    images = [keras_ocr.tools.read(image_path)]
    
    # Recognize text in the image
    prediction_groups = pipeline.recognize(images)
    
    
    fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))

    for ax, image, predictions in zip([axs], images, prediction_groups):
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
    plt.savefig('output.png')


if __name__ == "__main__":
    input_image = 'image.png'
    extract_text_from_image(input_image)