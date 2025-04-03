import os
import json
import numpy as np
from PIL import Image


def load_json_files(directory='block'):
    json_data = []
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist")
        return json_data
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    json_data.append(data)
            except Exception as e:
                print(f"Error loading {filename}: {str(e)}")
    
    return json_data

# Load all JSON files
json_files = load_json_files()

shapes = [data['image_shape'] for data in json_files]
# Find the maximum width and height
max_width = max(shape[1] for shape in shapes)
max_height = max(shape[0] for shape in shapes)

# Count PNG files in the block_img directory
png_count = sum(1 for file in os.listdir('block_img') if file.endswith('.png'))

# Create an empty array with maximum dimensions
merged_image = np.zeros((png_count,max_height, max_width), dtype=np.uint8)
i=0
order = []
# Load and process each image
for filename in os.listdir('block_img'):
    if filename.endswith('.png'):
        file_path = os.path.join('block_img', filename)
        print(file_path)
        order.append(int(filename.split('.')[0]))
        try:
            # Load image and convert to grayscale
            img = Image.open(file_path).convert('L')
            # Convert to numpy array
            img_array = np.array(img)
            # Get image dimensions
            h, w = img_array.shape
            # Place image in the merged array
            temp_array = np.zeros((max_height, max_width), dtype=np.uint8)
            # Calculate padding
            pad_height = (max_height - h) // 2
            pad_width = (max_width - w) // 2
            # Pad the image to center it
            img_array = np.pad(img_array, ((pad_height, max_height - h - pad_height), (pad_width, max_width - w - pad_width)), mode='constant', constant_values=255)
            rotated_img = np.flipud(img_array)
            # Convert to uint8
            img_array = rotated_img.astype(np.uint8)

            merged_image[i,:,:] = img_array
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
        i+=1


print(order)
# Create a dictionary to map order values to indices
order_dict = {value: idx for idx, value in enumerate(order)}
# Sort order and get the new indices
sorted_order = sorted(order)
sorted_indices = [order_dict[value] for value in sorted_order]
print(sorted_indices)
# Reorder merged_image according to sorted indices
print(np.average(merged_image[0]))
merged_image = merged_image[sorted_indices,:,:]
print(np.average(merged_image[0]))
np.save('merged_block_img.npy', merged_image)
    