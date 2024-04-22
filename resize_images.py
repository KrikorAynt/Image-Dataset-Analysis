from PIL import Image
import os
import sys
#import pandas as pd


# Function to resize an image
def resize_image(image, scale_factor):
    width, height = image.size
    new_width = int(width / scale_factor)
    new_height = int(height / scale_factor)
    return image.resize((new_width, new_height))


# Function to process images in a folder
def process_images(folder_path):
    # Create folder for resized images
    fourx_folder = os.path.join(folder_path, '4x')
    eightx_folder = os.path.join(folder_path, '8x')
    os.makedirs(fourx_folder, exist_ok=True)
    os.makedirs(eightx_folder, exist_ok=True)
    total_files = sum(1 for filename in os.listdir(folder_path) if filename.endswith('.tif'))
    # Process each image
    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'):
            image_path = os.path.join(folder_path, filename)
            # Open image
            image = Image.open(image_path)

            original_size = image.size

            # Resize image to be 4x smaller
            smaller_image4 = resize_image(image, 4)
            smaller_image4 = smaller_image4.resize((int(original_size[0]), int(original_size[1])))
            smaller_image4.save(os.path.join(fourx_folder, filename))
            # Resize image to be 8x smaller
            smaller_image8 = resize_image(image, 8)
            smaller_image8 = smaller_image8.resize((int(original_size[0]), int(original_size[1])))
            smaller_image8.save(os.path.join(eightx_folder, filename))


if len(sys.argv) >= 2:
    folder_path = sys.argv[1]
else:
    folder_path = r'./OSCD/'

if not os.path.isdir(folder_path):
    print("Error: Provided path is not a directory.")
    sys.exit(1)

# Process images in the provided folder
#folders = pd.read_csv(folder_path + 'all.txt')
folders = "aguasclaras", "bercy", "bordeaux", "nantes", "paris", "rennes", "saclay_e", "abudhabi", "cupertino", "pisa",\
    "beihai", "hongkong", "beirut", "mumbai", "brasilia", "montpellier", "norcia", "rio", "saclay_w", "valencia", "dubai",\
    "lasvegas", "milano", "chongqing"
for folder in folders:
    new_path = folder_path + '/' + folder + '/imgs_2/'
    new_path_rect = folder_path + '/' + folder + '/imgs_2_rect/'
    print(new_path)
    process_images(new_path)
    process_images(new_path_rect)
