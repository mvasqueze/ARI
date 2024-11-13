import pandas as pd
import re
from datetime import datetime
from cedulas_duplicadas import find_duplicate_cedulas

def fill_missing_info(duplicate_records, date_column):
    # Columnas relacionadas con el cuidador a ignorar si "Tiene cuidador" es "No"
    caretaker_columns = [
        "Nombres y apellidos del cuidador", "Documento del Cuidador", 
        "Parentezco del cuidador con la PcD", "Telefono del cuidador",
        "Como cuidador ¿ha visto afectada su salud?", "¿De que manera?", 
        "¿Ha visto limitadas sus posibilidades de ingreso economico?", 
        "¿Por que?", "¿Ha recibido capacitacion como cuidador?", 
        "Actividad Laboral del Cuidador", "Describa su emprendimiento",
        "Hace parte del comite municipal de Discapacidad",
        "Hace parte de alguna Organizacion/Asociacion de PcD",
        "Como se llama la Organizacion/Asociacion", 
        "Programas sociales en los que participa", 
        "Cual o Cuales programas sociales", 
        "A qué espacios de participación pertenece"
    ]
    
    # Ordenar por fecha en orden descendente para tener la fila más reciente primero
    duplicate_records = duplicate_records.sort_values(by=[date_column], ascending=False)
    
    # Agrupar por 'extracted_cedula' para manejar cada duplicado por separado
    filled_records = []
    
    for cedula, group in duplicate_records.groupby('extracted_cedula'):
        # Usar el primer (más reciente) registro como base
        most_recent_record = group.iloc[0].copy()
        
        # Determinar si las columnas del cuidador deben ser ignoradas según "Tiene cuidador"
        if most_recent_record.get("Tiene cuidador") == "No":
            columns_to_ignore = caretaker_columns
        else:
            columns_to_ignore = []
        
        # Identificar columnas con valores faltantes en el registro más reciente, excluyendo columns_to_ignore
        missing_columns = [
            col for col in most_recent_record.index 
            if pd.isnull(most_recent_record[col]) and col not in columns_to_ignore
        ]
        
        # Rastrear si se realizan cambios
        changes_made = False
        # Eliminar 'extracted_cedula' de la copia de original_row para evitar imprimirlo
        original_row = most_recent_record[missing_columns].copy()
        
        # Llenar valores faltantes a partir de registros más antiguos si hay columnas faltantes
        for _, row in group.iloc[1:].iterrows():
            before_filling = most_recent_record[missing_columns].copy()
            most_recent_record[missing_columns] = most_recent_record[missing_columns].combine_first(row[missing_columns])
            after_filling = most_recent_record[missing_columns]
            
            # Verificar si se llenaron valores
            if not before_filling.equals(after_filling):
                changes_made = True
        
        # Imprimir como tabla solo si se realizaron cambios
        if changes_made:
            filled_columns = [col for col in missing_columns if most_recent_record[col] is not None]
            print(f"\nCédula: {cedula}")
            
            # Crear un DataFrame para mostrar antes y después
            comparison_df = pd.DataFrame({
                "Before Filling": original_row,
                "After Filling": most_recent_record[missing_columns]
            })
            
            # Mostrar la tabla con solo columnas relevantes (excluyendo 'extracted_cedula')
            print(comparison_df[['Before Filling', 'After Filling']])
        
        # Agregar el registro lleno a la lista de resultados
        filled_records.append(most_recent_record)
    
    # Convertir la lista de registros llenos de nuevo a un DataFrame
    filled_records_df = pd.DataFrame(filled_records)
    
    # Devolver el DataFrame lleno
    return filled_records_df


if __name__ == "__main__":
    file_path = "../pcd_1211.csv"
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    filled_duplicate_records = fill_missing_info(duplicate_records, "Fecha de la encuesta")

    # Mostrar los registros llenos
    print("\nFilled records:")
    print(filled_duplicate_records.columns)
