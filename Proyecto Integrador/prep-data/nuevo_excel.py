import pandas as pd
import re
from datetime import datetime
from cedulas_duplicadas import find_duplicate_cedulas
from merge_cedulas import fill_missing_info

def limpiar_filas_vacias(df, verbose=True):
    """
    Elimina las filas donde 'Primer nombre de la PcD' está vacío
    
    Args:
        df (pandas.DataFrame): DataFrame original
        verbose (bool): Si True, muestra información detallada
        
    Returns:
        pandas.DataFrame: DataFrame sin las filas vacías
    """
    columna_nombre = "Primer nombre de la PcD"
    if columna_nombre not in df.columns:
        print("Columnas disponibles:", df.columns)
        raise ValueError(f"La columna '{columna_nombre}' no existe en el DataFrame.")
    
    # Crear máscaras para cada tipo de valor vacío
    mask_na = df[columna_nombre].isna()
    mask_null = df[columna_nombre].isnull()
    mask_empty = df[columna_nombre].astype(str).str.strip() == ''
    
    if verbose:
        print(f"Encontrados:")
        print(f"- {mask_na.sum()} valores NaN")
        print(f"- {mask_null.sum()} valores NULL")
        print(f"- {mask_empty.sum()} strings vacíos")
    
    # Combinar las máscaras y eliminar las filas
    mask_total = ~(mask_na | mask_null | mask_empty)
    df_limpio = df[mask_total]
    
    if verbose:
        filas_eliminadas = len(df) - len(df_limpio)
        print(f"\nResumen:")
        print(f"- Filas originales: {len(df)}")
        print(f"- Filas eliminadas: {filas_eliminadas}")
        print(f"- Filas restantes: {len(df_limpio)}")
        
        if filas_eliminadas > 0 and verbose:
            print("\nEjemplos de filas eliminadas:")
            filas_vacias = df[~mask_total]
            print(filas_vacias[['ObjectID', columna_nombre]].head())
    
    return df_limpio

def create_clean_csv(file_path, filled_duplicate_records, output_filename="clean_data.csv"):
    # Leer los datos originales
    data = pd.read_csv(file_path, dtype=str, low_memory=False, encoding='utf-8', sep=';')
    
    # Borrar registros sin nombre
    original_data = limpiar_filas_vacias(data, verbose=False)

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