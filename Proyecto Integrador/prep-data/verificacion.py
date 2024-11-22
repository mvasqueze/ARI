import pandas as pd
import numpy as np
import coordenadas_arcgis as ag
import normalizar_texto as norm

def validate_coordinates(dataframe, antioquia_municipios):
    """
    Filters the dataset for rows where coordinates are 0.0, NaN, or outside Antioquia.
    
    Args:
        dataframe (pd.DataFrame): Dataset with 'x' and 'y' columns representing coordinates.
        antioquia_municipios (pd.DataFrame): Dataset containing normalized municipio names and their coordinates.

    Returns:
        pd.DataFrame: Rows that meet the validation criteria.
    """
    def is_outside_antioquia(row):
        if pd.isna(row['x']) or pd.isna(row['y']):
            return "NaN"
        if row['x'] == 0.0 or row['y'] == 0.0:
            return "Zero Coordinate"
        
        municipio = ag.reverse_geocode_municipio(row['x'], row['y'])
        normalized_municipio = norm.normalizar_texto(municipio)
        
        # Check if municipio is in Antioquia
        if normalized_municipio not in antioquia_municipios['Municipio'].values:
            return f"Outside Antioquia ({municipio})"
        return None

    # Apply validation
    dataframe['Validation Result'] = dataframe.apply(is_outside_antioquia, axis=1)

    # Filter rows where validation fails
    invalid_rows = dataframe[dataframe['Validation Result'].notnull()]
    return invalid_rows

def data_verification(row):
    x, y = row["x"], row["y"]
    id = row["ObjectID"]
    print("---------------------------------------------------------------------")
    print(f"Procesando object id {id}")
    invalid_states = [None, "", "0.0", "nan"]
    
    # Check if x or y is invalid
    if pd.isna(x) or pd.isna(y) or x in invalid_states or y in invalid_states:
        print(f"Coordenadas encontradas en el dataset original: {x}, {y}")
        
        municipio = row["Municipio_normalizado"]
        # Assuming asignar_municipio is a function that geocodes and returns new coordinates
        new_x, new_y = ag.geocode_municipio(municipio)
        
        print(f"Registro procesado: {id} \nCoordenadas previas: {x}, {y} \nNuevas coordenadas: {new_x}, {new_y}")
        
        # Update row with new coordinates
        row["x"], row["y"] = new_x, new_y

    return row

# Example usage
if __name__ == "__main__":
    # Load dataset with coordinates to validate
    dataset_path = "combined_data.xlsx"  # Replace with your dataset file path
    df = pd.read_excel(dataset_path)

    # Load Antioquia municipios dataset
    municipios_path = "geocoded_municipios.csv"  # Replace with your municipios dataset file path
    antioquia_municipios_df = pd.read_csv(municipios_path)

    # Validate coordinates
    invalid_coordinates_df = validate_coordinates(df, antioquia_municipios_df)

    # Print results
    print("Rows with invalid coordinates:")
    print(invalid_coordinates_df)

    # Optionally save invalid rows to a CSV
    invalid_coordinates_df.to_excel("invalid_coordinates.xlsx", index=False)
