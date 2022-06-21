import json, sys, os

if len(sys.argv) < 3:
	sys.exit("Usage: poly2geojson input.poly output.geojson")

input_path, output_path = sys.argv[1:]
if not os.path.isfile(input_path):
	sys.exit("File not found")

def poly2geojson(input_path, output_path):
	filename, _ = os.path.splitext(input_path)
	if not output_path.endswith(".geojson"):
		output_path += ".geojson"

	data = open(input_path, "r").readlines()[1:-1]

	country = {
		"type": "FeatureCollection",
		"features": [
			{
				"type": "Feature",
				"properties": {},
				"geometry": {
					"type": "MultiPolygon",
					"coordinates": []
				}
			}
		]
	}

	polygon = country["features"][0]["geometry"]
	region = []

	for line in data:
		line = line.strip()

		if line != "END":
			if len(line.split()) == 1:
				pass

			else:
				lat, lon = line.split()
				lat, lon = float(lat), float(lon)
				region.append((lat, lon))

		else:
			if len(region) > 0:
				country["features"][0]["geometry"]["coordinates"].append([region])

			region = []

	json.dump(country, open(output_path, "w+"), indent=4)

poly2geojson(input_path, output_path)
