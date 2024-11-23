import pandas as pd
from normalizar_texto import normalizar_texto  
from coordenadas_arcgis import geocode_municipio

# Load the original .csv file
file_path = "clean_pcd_data.csv"  # Replace with the path to your .csv file
df = pd.read_csv(file_path)

# Extract unique municipality names and normalize them
column_name = "Municipio de residencia (PcD)"
municipalities = df[column_name].dropna().unique()  # Remove NaN and get unique entries
normalized_municipalities = [normalizar_texto(municipio) for municipio in municipalities]

# Create a new DataFrame with "Municipio", "x", and "y" columns
new_df = pd.DataFrame({
    "Municipio": normalized_municipalities,
    "x": [None] * len(normalized_municipalities),
    "y": [None] * len(normalized_municipalities)
})

# Populate the "x" and "y" columns with geocoded coordinates
for index, row in new_df.iterrows():
    try:
        x, y = geocode_municipio(row["Municipio"])  # Call the geocoding function
        new_df.at[index, "x"] = x
        new_df.at[index, "y"] = y
    except Exception as e:
        print(f"Error geocoding {row['Municipio']}: {e}")
        new_df.at[index, "x"] = None
        new_df.at[index, "y"] = None

# Save the updated DataFrame to a new .csv file
output_file_path = "geocoded_municipios.csv"  # Replace with desired output file path
new_df.to_csv(output_file_path, index=False)

print(f"Geocoded dataset saved to {output_file_path}")

