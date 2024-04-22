import os
import json
from PIL import Image
import sys
from shapely.geometry import Polygon
from shapely.geometry import Point

Image.MAX_IMAGE_PIXELS = None
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']


def polygon_centroid(coords):
    poly = Polygon(coords)
    centroid = poly.centroid
    return centroid.x, centroid.y


def jsonify(dataset_path):
    images = {
        "images": []
    }

    def traverse_directory(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                traverse_directory(file_path)
            elif os.path.splitext(filename)[1].lower() in image_extensions:
                try:
                    json_name = os.path.splitext(filename)[0] + ".json"
                    json_name = os.path.join(directory, json_name)
                    with open(json_name, 'r') as file:
                        json_for_image = json.load(file)
                    location = json_for_image['raw_location']
                    if location.startswith("POLYGON"):
                        coords = [
                            [float(pair.split()[0]), float(pair.split()[1])]
                            for pair in location.strip("POLYGON ()").split(", ")
                        ]
                        lon, lat = polygon_centroid(coords)
                        location = {"Longitude": lon, "Latitude": lat}
                    info = {
                        "Name": json_for_image['img_filename'],
                        "Path": file_path,
                        "GSD": json_for_image['gsd'],
                        "Location": location,
                        "Width": json_for_image['img_width'],
                        "Height": json_for_image['img_height']
                    }
                    images["images"].append(info)
                    file.close()
                except Exception as e:
                    # print(f"Error processing {filename}: {e}")
                    try:
                        with Image.open(file_path) as img:
                            width, height = img.size
                        info = {
                            "Name": filename,
                            "Path": file_path,
                            "Width": width,
                            "Height": height
                        }
                        images["images"].append(info)
                        img.close()
                    except Exception as f:
                        print(f"Error with backup option for {filename}: {f}")

    # Start traversing from the root dataset path
    traverse_directory(dataset_path)
    with open(f"./{os.path.basename(os.path.normpath(dataset_path))}.json", 'w') as json_file:
        json.dump(images, json_file, indent=4)


if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    print("USAGE: python3 jsonify.py path/to/your/dataset/")
    exit(1)

jsonify(path)
