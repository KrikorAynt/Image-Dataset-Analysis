import json
import os
import sys
from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx


def plot_locations_from_json(json_file):
    # Load JSON data
    with open(json_file, "r") as file:
        dataset = json.load(file)

    # Filter out images without location data
    images_with_location = [image for image in dataset.get("images", []) if "Location" in image]

    # Generate geojson with markers for each image location
    geojson = dlx.dicts_to_geojson([{
        "type": "Feature",
        "properties": {
            "Name": image["Name"],
            "Path": image["Path"],
            "GSD": image["GSD"],
            "Width": image["Width"],
            "Height": image["Height"]
        },
        "lon": image["Location"]["Longitude"],
        "lat": image["Location"]["Latitude"],
        "tooltip": image["Name"] + "<br>" + str(image["Location"]["Longitude"]) + ", " + str(
            image["Location"]["Latitude"])
    } for image in images_with_location])

    # Create example app
    app = Dash(__name__)
    app.title = os.path.basename(os.path.normpath(json_file))
    # Create example app layout
    app.layout = html.Div([
        dl.Map(children=[
            dl.TileLayer(),
            dl.GeoJSON(
                data=geojson,
                cluster=True,  # Enable clustering
                zoomToBoundsOnClick=True,  # Zoom to cluster on click
                superClusterOptions={"radius": 100}  # Configure supercluster options
            )
        ], style={'height': '100vh'}, center=[40.0691, 45.0382], zoom=6),
    ])

    app.run_server(debug=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        plot_locations_from_json(json_file)
    else:
        print("USAGE: python3 plot_locations.py path/to/your/json_file")
