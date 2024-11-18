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
            print("API")
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
            print("BBOX")
            return query_result.features[0].attributes['NOMBRE_VER']
        return None
        
    except Exception as e:
        return None
    
def query_municipio(x, y):
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
            print(query_result.features[0].attributes)
            return query_result.features[0].attributes['NOMB_MPIO']
        return None
        
    except Exception as e:
        # Fallback to bounding box method if point query fails
        return query_with_bbox_municipio(vereda_layer, x, y)

def query_with_bbox_municipio(vereda_layer, x, y, offset=0.001):
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
            print(query_result.features[0].attributes)
            return query_result.features[0].attributes['NOMB_MPIO']
        return None
        
    except Exception as e:
        return None


# Método para consultar vereda usando el nombre y devolver coordenadas
def query_vereda_coordinates(nombre_vereda):
    # URL de la capa de veredas en ArcGIS
    layer_url = "https://services5.arcgis.com/K90UQIB09TmTjUL8/arcgis/rest/services/Veredas_de_Antioquia/FeatureServer/3"
    vereda_layer = FeatureLayer(layer_url)
    
    try:
        # Parámetros para consulta por nombre
        query_result = vereda_layer.query(
            where=f"NOMBRE_VER LIKE '%{nombre_vereda}%'",
            out_fields="*",
            return_geometry=True  # Necesitamos geometría para extraer coordenadas
        )
        
        # Verificar si se encuentran resultados
        if query_result.features:
            print("Consulta exitosa")
            
            # Obtener el polígono de la geometría del primer resultado
            geometry = query_result.features[0].geometry
            if geometry and 'rings' in geometry:
                # Calcular el centroide del polígono
                rings = geometry['rings']
                centroid = calculate_centroid(rings)
                return centroid  # Devuelve coordenadas (x, y)
            else:
                print("Geometría no encontrada")
                return None
        else:
            print("No se encontraron coincidencias")
            return None
        
    except Exception as e:
        print(f"Error al consultar la API de ArcGIS: {e}")
        return None

# Método para consultar vereda usando el nombre y devolver coordenadas
def query_municipio_coordinates(nombre_municipio):
    # URL de la capa de veredas en ArcGIS
    layer_url = "https://services5.arcgis.com/K90UQIB09TmTjUL8/arcgis/rest/services/Veredas_de_Antioquia/FeatureServer/3"
    vereda_layer = FeatureLayer(layer_url)
    
    try:
        # Parámetros para consulta por nombre
        query_result = vereda_layer.query(
            where=f"NOMB_MPIO LIKE '%{nombre_municipio}%'",
            out_fields="*",
            return_geometry=True  # Necesitamos geometría para extraer coordenadas
        )
        
        # Verificar si se encuentran resultados
        if query_result.features:
            print("Consulta exitosa")
            
            # Obtener el polígono de la geometría del primer resultado
            geometry = query_result.features[0].geometry
            if geometry and 'rings' in geometry:
                # Calcular el centroide del polígono
                rings = geometry['rings']
                centroid = calculate_centroid(rings)
                return centroid  # Devuelve coordenadas (x, y)
            else:
                print("Geometría no encontrada")
                return None
        else:
            print("No se encontraron coincidencias")
            return None
        
    except Exception as e:
        print(f"Error al consultar la API de ArcGIS: {e}")
        return None

# Método para calcular el centroide a partir de los vértices del polígono
def calculate_centroid(rings):
    # Los anillos son listas de coordenadas [(x1, y1), (x2, y2), ...]
    x_coords = []
    y_coords = []
    
    for ring in rings:
        for x, y in ring:
            x_coords.append(x)
            y_coords.append(y)
    
    # Centroide (promedio de las coordenadas)
    centroid_x = sum(x_coords) / len(x_coords)
    centroid_y = sum(y_coords) / len(y_coords)
    return (centroid_x, centroid_y)

import pandas as pd

def identificar_zona_urbana(dataset):
    columna_zona="Zona de residencia (PcD)"
    if columna_zona not in dataset.columns:
        raise ValueError(f"La columna '{columna_zona}' no existe en el dataset.")
    
    # Crear una nueva columna con True si es urbana y False si es rural
    dataset["Es_Urbana"] = dataset[columna_zona].str.strip().str.lower() == "urbana"
    
    return dataset

# Ejemplo de uso
file_path = "clean_pcd_data.csv"
dataset = pd.read_csv(file_path, delimiter=";", dtype=str, encoding="utf-8")

# Aplicar el método
dataset_actualizado = identificar_zona_urbana(dataset)

# Verificar las primeras filas
print(dataset_actualizado[["Zona de residencia (PcD)", "Es_Urbana"]].head())

# Guardar el dataset actualizado (opcional)
dataset_actualizado.to_csv("clean_pcd_data_actualizado.csv", index=False, encoding="utf-8", sep=";")


# Ejemplo de uso
'''nombre_vereda = "La Seca"
nombre_municipio = "Bello"
coordenadas = query_municipio_coordinates(nombre_municipio)

if coordenadas:
    #print(f"Coordenadas de la vereda '{nombre_vereda}': {coordenadas}")
    print(f"Coordenadas del municipio '{nombre_municipio}': {coordenadas}")
else:
    print("No se encontraron las coordenadas de la vereda especificada.")'''


# Example usage
x, y = -75.5310, 6.3013
vereda_name = query_municipio(x, y)
if vereda_name:
    print(f"Found vereda: {vereda_name}")
else:
    print("No vereda found at these coordinates")

