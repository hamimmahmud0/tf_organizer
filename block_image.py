import json, sys
from PIL import Image 

# Load the JSON file
with open('block/{}.json'.format(sys.argv[1]), 'r') as file:
    info = json.load(file)

image_shape = info['image_shape']
boxes = info['boxes']
# Create a blank image with the specified shape
image = Image.new('RGB', (image_shape[1], image_shape[0]), (255, 255, 255))
# Draw the boxes on the image
for box in boxes:
    # Convert the box coordinates to integers
    x1, y1 = int(box['x1']), int(box['y1'])
    x2, y2 = int(box['x2']), int(box['y2'])
    x3, y3 = int(box['x3']), int(box['y3'])
    x4, y4 = int(box['x4']), int(box['y4'])
    
    # Draw the box on the image
    image.paste((0, 0, 0), [x1, y1, x3, y3])  # Top-left to bottom-right
    #image.paste((0, 255, 0), [x2, y2, x4, y4])  # Top-right to bottom-left
# Save the image
image.save('block_img/{}.png'.format(sys.argv[1]))
# Display the image
image.show()