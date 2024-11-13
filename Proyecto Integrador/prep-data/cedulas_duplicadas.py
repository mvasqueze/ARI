import pandas as pd
import re
from datetime import datetime

def find_duplicate_cedulas(file_path):

    # Leer el archivo CSV
    df = pd.read_csv(file_path,
                     delimiter=';', 
                     dtype=str,  # Leer todas las columnas como strings
                     low_memory=False,  # Prevenir advertencias
                     encoding='utf-8')
    
    # Se verifica que la columna "Numero de documento (PcD)", que se refiere a la PcD, se encuentre en el dataset.
    column_name = 'Numero de documento (PcD)'  
    if column_name not in df.columns:
        raise KeyError(f"Columna '{column_name}' no encontrada en el archivo. Por favor, verifique el nombre de la columna.")
    
    # Si la columna existe, se establece como la que va a ser usada
    df['extracted_cedula'] = df[column_name]
    
    # Identificar duplicados: Se cuenta cuántas veces aparece una cédula y se agregan a la lista de duplicados aquellos que aparezcan más de una vez
    duplicates = df['extracted_cedula'].value_counts()
    duplicates = duplicates[duplicates > 1]
    
    # Registro completo de cada duplicado: Se extraen los registros completos de las cédulas duplicadas
    duplicate_records = df[df['extracted_cedula'].isin(duplicates.index)]
    
    # Generar archivo nuevo con los registros duplicados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'listado_cedulas_duplicadas_{timestamp}.csv'
    
    if len(duplicate_records) > 0:
        duplicate_records.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"\nLos registros duplicados han sido guardados en: {output_filename}")
    
    return duplicates, duplicate_records, output_filename

# Ejemplo de uso
if __name__ == "__main__":
    file_path = "../pcd_1211.csv"  # Reemplazar con la ruta de su archivo
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    
    print("\nCédulas duplicadas encontradas:")
    if len(duplicates) > 0:
        print(duplicates)
        print(f"\nNúmero de registros duplicados: {len(duplicate_records)}")
    else:
        print("No se encontraron cédulas duplicadas")
    
    print(f"\nTotal de registros procesados: {len(duplicate_records)}")
