import pandas as pd
import re
from datetime import datetime
from cedulas_duplicadas import find_duplicate_cedulas

def fill_missing_info(duplicate_records, date_column):
    # Columns related to the caretaker to ignore if "Tiene cuidador" is "No"
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
    
    # Sort by date in descending order to have the most recent row for each cédula first
    duplicate_records = duplicate_records.sort_values(by=[date_column], ascending=False)
    
    # Group by 'extracted_cedula' to handle each duplicate separately
    filled_records = []
    
    for cedula, group in duplicate_records.groupby('extracted_cedula'):
        # Use the first (most recent) record as the base
        most_recent_record = group.iloc[0].copy()
        
        # Determine if caretaker columns should be ignored based on "Tiene cuidador"
        if most_recent_record.get("Tiene cuidador") == "No":
            columns_to_ignore = caretaker_columns
        else:
            columns_to_ignore = []
        
        # Identify columns with missing values in the most recent record, excluding columns_to_ignore
        missing_columns = [
            col for col in most_recent_record.index 
            if pd.isnull(most_recent_record[col]) and col not in columns_to_ignore
        ]
        
        # Track whether any changes are made
        changes_made = False
        # Remove 'extracted_cedula' from the original_row copy to avoid printing it
        original_row = most_recent_record[missing_columns].copy()
        
        # Fill missing values from older records if there are missing columns
        for _, row in group.iloc[1:].iterrows():
            before_filling = most_recent_record[missing_columns].copy()
            most_recent_record[missing_columns] = most_recent_record[missing_columns].combine_first(row[missing_columns])
            after_filling = most_recent_record[missing_columns]
            
            # Check if any values were filled
            if not before_filling.equals(after_filling):
                changes_made = True
        
        # Print as a table only if changes were made
        if changes_made:
            filled_columns = [col for col in missing_columns if most_recent_record[col] is not None]
            print(f"\nCédula: {cedula}")
            
            # Create a DataFrame to show before and after
            comparison_df = pd.DataFrame({
                "Before Filling": original_row,
                "After Filling": most_recent_record[missing_columns]
            })
            
            # Display the table with only relevant columns (excluding 'extracted_cedula')
            print(comparison_df[['Before Filling', 'After Filling']])
        
        # Append the filled record to the results list
        filled_records.append(most_recent_record)
    
    # Convert the list of filled records back into a DataFrame
    filled_records_df = pd.DataFrame(filled_records)
    
    
    # Return the filled DataFrame
    return filled_records_df


if __name__ == "__main__":
    file_path = "../pcd_1211.csv"
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    filled_duplicate_records = fill_missing_info(duplicate_records, "Fecha de la encuesta")

    # Display the filled records
    print("\nFilled records:")
    print(filled_duplicate_records.columns)

    
