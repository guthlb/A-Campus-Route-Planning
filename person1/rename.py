import os
import json
import networkx as nx
from pyproj import Transformer
from geopy.distance import geodesic

# =========================
# PATH SETUP
# =========================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

graph_path = os.path.join(base_dir, "data", "mit_clean.graphml")

geojson_files = [
    "Academic_Blocks.geojson",
    "Hostels.geojson",
    "Mess.geojson"
]

# =========================
# LOAD GRAPH
# =========================
G = nx.read_graphml(graph_path)
print(f"Graph loaded: {len(G.nodes())} nodes")

# =========================
# COORDINATE CONVERTER
# =========================
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

def convert_if_needed(lon, lat):
    if abs(lon) > 180 or abs(lat) > 90:
        lon, lat = transformer.transform(lon, lat)
    return lat, lon

# =========================
# EXTRACT PLACES
# =========================
def extract_places(file_path):
    places = []

    with open(file_path) as f:
        data = json.load(f)

    for feature in data["features"]:
        props = feature.get("properties", {})

        name = (
            props.get("Name") or
            props.get("Name/Num") or
            props.get("Shops")
        )

        if not name:
            continue

        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [])

        if not coords:
            continue

        try:
            if geom["type"] == "Point":
                lon, lat = coords

            elif geom["type"] == "Polygon":
                lon, lat = coords[0][0]

            elif geom["type"] == "MultiPolygon":
                lon, lat = coords[0][0][0]

            else:
                continue

            lat, lon = convert_if_needed(lon, lat)

            places.append((name.strip(), lat, lon))

        except Exception:
            continue

    return places

# =========================
# LOAD ALL PLACES
# =========================
all_places = []

for file in geojson_files:
    path = os.path.join(base_dir, "data", file)
    extracted = extract_places(path)
    print(f"{file}: {len(extracted)} places loaded")
    all_places.extend(extracted)

print(f"Total places: {len(all_places)}")

# =========================
# RESET LABELS
# =========================
for node in G.nodes():
    G.nodes[node]["label"] = "Unknown"

# =========================
# ASSIGN ONE NODE PER PLACE
# =========================
print("Assigning ONE node per place...")

assigned_nodes = set()

for name, plat, plon in all_places:

    best_node = None
    min_dist = float("inf")

    for node, data in G.nodes(data=True):

        if node in assigned_nodes:
            continue

        try:
            lat = float(data["y"])
            lon = float(data["x"])
        except:
            continue

        d = geodesic((lat, lon), (plat, plon)).meters

        if d < min_dist:
            min_dist = d
            best_node = node

    if best_node is not None:
        G.nodes[best_node]["label"] = name
        assigned_nodes.add(best_node)

print("Assignment complete!")

# =========================
# SAVE GRAPH
# =========================
output_path = os.path.join(base_dir, "data", "mit_labeled.graphml")
nx.write_graphml(G, output_path)

print(f"Saved labeled graph → {output_path}")