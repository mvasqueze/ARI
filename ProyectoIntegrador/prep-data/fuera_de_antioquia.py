import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import requests
import io

def download_antioquia_boundary():
    """
    Downloads Antioquia's boundary from OpenStreetMap through Nominatim API
    Returns a GeoDataFrame with Antioquia's polygon
    """
    # Get Antioquia's boundary from OSM
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["name"="Colombia"]->.country;
    rel["admin_level"="4"]["name"="Antioquia"](area.country);
    out geom;
    """
    
    response = requests.post(overpass_url, data=overpass_query)
    
    # Convert to GeoDataFrame
    antioquia = gpd.read_file(io.StringIO(response.text))
    return antioquia

def main():
    # Example usage
    # Read your Excel file
    try:
        antioquia = download_antioquia_boundary()
    except Exception as e:
        print(f"Auxilio! Algo pasó: {e}")

if __name__ == "__main__":
    main()

'''
def validate_coordinates(coords_df, geometry_col='geometry'):
    """
    Validates if points are inside Antioquia's boundary
    
    Parameters:
    coords_df: DataFrame with 'x' and 'y' columns for longitude and latitude
    geometry_col: name of the geometry column in the result
    
    Returns:
    GeoDataFrame with original data plus validation results
    """
    # Convert coordinates to GeoDataFrame
    geometry = [Point(xy) for xy in zip(coords_df['x'], coords_df['y'])]
    gdf = gpd.GeoDataFrame(coords_df, geometry=geometry, crs="EPSG:4326")
    
    # Get Antioquia's boundary
    antioquia = download_antioquia_boundary()
    
    # Perform spatial join to check which points are inside
    gdf['is_inside_antioquia'] = gdf.within(antioquia.unary_union)
    
    # For points outside, calculate distance to boundary and suggest nearest point
    if not gdf['is_inside_antioquia'].all():
        boundary = antioquia.unary_union
        outside_points = gdf[~gdf['is_inside_antioquia']]
        
        # Calculate nearest points on boundary
        nearest_points = [boundary.interpolate(boundary.project(point))
                        for point in outside_points.geometry]
        
        # Add suggested coordinates for points outside
        gdf.loc[~gdf['is_inside_antioquia'], 'suggested_x'] = [p.x for p in nearest_points]
        gdf.loc[~gdf['is_inside_antioquia'], 'suggested_y'] = [p.y for p in nearest_points]
    
    return gdf
'''


