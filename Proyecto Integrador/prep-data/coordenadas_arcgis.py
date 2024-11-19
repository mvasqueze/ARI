from arcgis.features import FeatureLayer
from arcgis.geometry import Point


# Connect to the vereda layer
vereda_layer_url = "https://services5.arcgis.com/K90UQIB09TmTjUL8/arcgis/rest/services/Veredas_de_Antioquia/FeatureServer/3"
vereda_layer = FeatureLayer(vereda_layer_url)

print(vereda_layer.properties)

# Example coordinates (replace with your data)
x, y = -75.567, 6.244  # Longitude, Latitude

# Create a Point geometry
point = Point({"x": x, "y": y, "spatialReference": {"wkid": 4326}})

# Query the vereda layer
query_result = vereda_layer.query(geometry_filter={
    "geometry": point,
    "spatialRelationship": "esriSpatialRelIntersects"
})

# Check results
if query_result.features:
    for feature in query_result.features:
        print(f"Vereda Name: {feature.attributes['vereda_name']}")
        print(f"Municipio Name: {feature.attributes['municipio_name']}")
else:
    print("No matching vereda found.")
