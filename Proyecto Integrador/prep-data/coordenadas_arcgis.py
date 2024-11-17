from arcgis.features import FeatureLayer

def query_vereda(x, y):
    layer_url = "https://services5.arcgis.com/K90UQIB09TmTjUL8/arcgis/rest/services/Veredas_de_Antioquia/FeatureServer/3"
    vereda_layer = FeatureLayer(layer_url)
    
    # REST API style parameters (working method)
    geom_params = {
        "geometryType": "esriGeometryPoint",
        "geometry": f"{x},{y}",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects"
    }
    
    try:
        query_result = vereda_layer.query(
            where="1=1",
            out_fields="*",
            **geom_params
        )
        
        if query_result.features:
            return query_result.features[0].attributes['NOMBRE_VER']
        return None
        
    except Exception as e:
        # Fallback to bounding box method if point query fails
        return query_with_bbox(vereda_layer, x, y)

def query_with_bbox(vereda_layer, x, y, offset=0.001):
    bbox = {
        "xmin": x - offset,
        "ymin": y - offset,
        "xmax": x + offset,
        "ymax": y + offset,
        "spatialReference": {"wkid": 4326}
    }
    
    try:
        query_result = vereda_layer.query(
            where="1=1",
            out_fields="*",
            return_geometry=True,
            geometry=bbox,
            geometry_type="esriGeometryEnvelope"
        )
        
        if query_result.features:
            return query_result.features[0].attributes['NOMBRE_VER']
        return None
        
    except Exception as e:
        return None

# Example usage
x, y = -75.43, 5.78
vereda_name = query_vereda(x, y)
if vereda_name:
    print(f"Found vereda: {vereda_name}")
else:
    print("No vereda found at these coordinates")