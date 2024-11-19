from arcgis.features import FeatureLayer
import pandas as pd

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
                return True, centroid  # Devuelve coordenadas (x, y)
            else:
                print("Geometría no encontrada")
                return False, None
        else:
            print("No se encontraron coincidencias")
            return False, None
        
    except Exception as e:
        print(f"Error al consultar la API de ArcGIS: {e}")
        return False, None

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

def identificar_zona_urbana(row, columna_zona="Zona de residencia (PcD)"):
    """
    Identifica si una fila corresponde a zona urbana
    
    Args:
        row: Fila del DataFrame
        columna_zona: Nombre de la columna que contiene la zona
    
    Returns:
        bool: True si es urbana, False si no
    """
    if columna_zona not in row.index:
        raise ValueError(f"La columna '{columna_zona}' no existe en la fila.")
    
    return row[columna_zona].strip().lower() == "urbana"

def dividir_por_zona(df, columna_zona="Zona de residencia (PcD)"):
    """
    Divide un DataFrame en dos basándose en la zona de residencia.
    
    Args:
        df: DataFrame a dividir
        columna_zona: Nombre de la columna que contiene la zona
    """
    # Aplicar la función de clasificación a todo el dataset
    mask_urbana = df.apply(lambda row: identificar_zona_urbana(row, columna_zona), axis=1)
    
    # Dividir el dataset
    df_urbano = df[mask_urbana]
    df_rural = df[~mask_urbana]
    
    return df_urbano, df_rural

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

