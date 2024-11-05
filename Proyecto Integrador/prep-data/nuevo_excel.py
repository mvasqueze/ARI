import pandas as pd
import re
from datetime import datetime
from cedulas_duplicadas import find_duplicate_cedulas
from merge_cedulas import fill_missing_info

def create_clean_csv(file_path, filled_duplicate_records, output_filename="clean_data.csv"):
    # Read the original data
    original_data = pd.read_csv(file_path, dtype=str, low_memory=False, encoding='utf-8')
    
    # Filter out duplicate records by keeping only those not in 'filled_duplicate_records'
    non_duplicates = original_data[~original_data['Numero de documento (PcD)'].isin(filled_duplicate_records['Numero de documento (PcD)'])]
    
    # Combine the non-duplicate records with the filled duplicate records
    clean_data = pd.concat([non_duplicates, filled_duplicate_records], ignore_index=True)
    
    # Save the combined data to a new CSV file
    clean_data.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Cleaned data saved to {output_filename}")

if __name__ == "__main__":
    file_path = "../pcd_0411.csv"
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    filled_duplicate_records = fill_missing_info(duplicate_records, "Fecha de la encuesta")
    create_clean_csv(file_path, filled_duplicate_records, output_filename="clean_pcd_data.csv")

    # Display the filled records
    print("\nFilled records:")
    print(filled_duplicate_records)