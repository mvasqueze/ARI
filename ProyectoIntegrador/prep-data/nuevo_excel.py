import pandas as pd
import re
from datetime import datetime
from cedulas_duplicadas import find_duplicate_cedulas
from merge_cedulas import fill_missing_info

def create_clean_csv(file_path, filled_duplicate_records, output_filename="clean_data.csv"):
    # Leer los datos originales
    original_data = pd.read_csv(file_path, dtype=str, low_memory=False, encoding='utf-8', sep=';')

    # Filtrar los registros duplicados manteniendo solo aquellos que no están en 'filled_duplicate_records'
    non_duplicates = original_data[~original_data['Numero de documento (PcD)'].isin(filled_duplicate_records['Numero de documento (PcD)'])]
    
    # Combinar los registros no duplicados con los registros duplicados obtenidos después del merge
    clean_data = pd.concat([non_duplicates, filled_duplicate_records], ignore_index=True)
    
    # Guardar los datos combinados en un nuevo archivo CSV
    clean_data.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Datos limpiados guardados en {output_filename}")

if __name__ == "__main__":
    file_path = "../pcd_1211.csv"
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)


    filled_duplicate_records = fill_missing_info(duplicate_records, "Fecha de la encuesta")
    create_clean_csv(file_path, filled_duplicate_records, output_filename="clean_pcd_data.csv")

    # Display the filled records
    print("\nFilled records:")
    print(filled_duplicate_records)