import pandas as pd
import re
from datetime import datetime

def find_duplicate_cedulas(file_path):
    # Read the CSV file with mixed types handling
    df = pd.read_csv(file_path,
                     delimiter=';', 
                     dtype=str,  # Read all columns as strings to avoid mixed type issues
                     low_memory=False,  # Prevent mixed type warnings
                     encoding='utf-8')
    
    # Try using the exact name for the "Numero de documento (PcD)" column after confirming it
    column_name = 'Numero de documento (PcD)'  # Adjust if needed based on printed output
    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' not found in the file. Please verify the column name.")
    
    # Directly use the correct column to find duplicates
    df['extracted_cedula'] = df[column_name]
    
    # Identify duplicates
    duplicates = df['extracted_cedula'].value_counts()
    duplicates = duplicates[duplicates > 1]
    
    # Complete record of each duplicate
    duplicate_records = df[df['extracted_cedula'].isin(duplicates.index)]
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'listado_cedulas_duplicadas_{timestamp}.csv'
    
    # Save duplicate records to CSV
    if len(duplicate_records) > 0:
        duplicate_records.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"\nDuplicate records have been saved to: {output_filename}")
    
    return duplicates, duplicate_records, output_filename

# Example usage
if __name__ == "__main__":
    file_path = "../pcd_1211.csv"  # Replace with your file path
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    
    print("\nDuplicate cédulas found:")
    if len(duplicates) > 0:
        print(duplicates)
        print(f"\nNumber of duplicate records: {len(duplicate_records)}")
    else:
        print("No duplicate cédulas found")
    
    print(f"\nTotal records processed: {len(duplicate_records)}")
