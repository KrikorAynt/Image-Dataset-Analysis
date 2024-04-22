import sys
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']


def calculate_image_statistics(dataset_path):
    total_images = 0
    total_pixels = 0
    unique_formats = set()

    # Recursive function to traverse directories
    def traverse_directory(directory):
        nonlocal total_images, total_pixels, unique_formats
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                # Recursively traverse subdirectories
                traverse_directory(file_path)
            elif os.path.splitext(filename)[1].lower() in image_extensions:
                total_images += 1
                try:
                    with Image.open(file_path) as img:
                        # Get image dimensions
                        width, height = img.size
                        total_pixels += width * height

                        # Get image format
                        format = img.format
                        # Add format to the set of unique formats
                        unique_formats.add(format)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    # Start traversing from the root dataset path
    traverse_directory(dataset_path)

    return total_images, total_pixels, unique_formats


def calculate_image_statistics_per_folder(dataset_path):
    folder_statistics = {}

    # Recursive function to traverse directories
    def traverse_directory(directory):
        nonlocal folder_statistics
        for dirpath, dirnames, filenames in os.walk(directory):
            total_images = 0
            total_pixels = 0
            unique_formats = set()
            for filename in filenames:
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.tif'):
                    total_images += 1
                    try:
                        with Image.open(os.path.join(dirpath, filename)) as img:
                            # Get image dimensions
                            width, height = img.size
                            total_pixels += width * height

                            # Get image format
                            format = img.format
                            # Add format to the set of unique formats
                            unique_formats.add(format)
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
            if total_images > 0:
                folder_statistics[dirpath] = {
                    'total_images': total_images,
                    'total_pixels': total_pixels,
                    'unique_formats': unique_formats}

    # Start traversing from the root dataset path
    traverse_directory(dataset_path)

    return folder_statistics


if len(sys.argv) >= 3:
    mode = int(sys.argv[1])
    dataset_path = sys.argv[2]
elif len(sys.argv) >= 2:
    mode = int(sys.argv[1])
    dataset_path = "./"
    print("Default filepath. Proper usage:")
    print(f"python3 dataset_analyzer.py {mode} <FILEPATH>")
else:
    mode = 0
    dataset_path = "./"
    print("Default filepath and mode selected. Proper usage:")
    print("python3 dataset_analyzer.py <MODE> <FILEPATH>")
    print("Mode 0: Total dataset stats    Mode 1: Stats per child folder")

if not (mode == 0 or mode == 1):
    print("Error: Invalid mode. Options: 0 | 1")
    sys.exit(1)

if not os.path.isdir(dataset_path):
    print("Error: Provided path is not a directory.")
    sys.exit(1)

if mode == 0:
    total_images, total_pixels, unique_formats = calculate_image_statistics(dataset_path)
    print(f"Total images: {total_images}")
    print(f"Total pixels: {total_pixels}")
    print("Unique image formats:")
    for format in unique_formats:
        print(format)
elif mode == 1:
    folder_statistics = calculate_image_statistics_per_folder(dataset_path)
    for folder, stats in folder_statistics.items():
        print(f"Folder: {folder}")
        print(f"Total images: {stats['total_images']}")
        print(f"Total pixels: {stats['total_pixels']}")
        print("Unique image formats:")
        for format in stats['unique_formats']:
            print(format)

