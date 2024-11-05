import pandas as pd
import re
from datetime import datetime

def find_duplicate_cedulas(file_path):
    # Read the CSV file with mixed types handling
    df = pd.read_csv(file_path, 
                     dtype=str,  # Read all columns as strings to avoid mixed type issues
                     low_memory=False,  # Prevent mixed type warnings
                     encoding='utf-8')
    
    # Function to extract cédula from the relevant columns
    def extract_cedula(row):
        # Convert row to string and look for patterns like "Cédula 12345" or "Cédula de ciudadanía 12345"
        row_str = ' '.join([str(val) for val in row.values])
        
        # Pattern to match "Cédula" or "Cédula de ciudadanía" followed by numbers
        matches = re.finditer(r'Cedula(?:\s+de\s+ciudadania)?\s+(\d[\d\.E\+]+)', row_str)
        
        cedulas = []
        for match in matches:
            try:
                # Handle both normal numbers and scientific notation
                cedula = str(int(float(match.group(1))))
                # Exclude the encuestador's cédula (appears first in the row)
                if not cedulas:  # Skip the first cédula (encuestador)
                    cedulas.append(cedula)
                    continue
                return cedula
            except ValueError:
                continue
        return None

    # Extract cédulas from each row
    df['extracted_cedula'] = df.apply(extract_cedula, axis=1)
    
    # Lista de cédulas duplicadas
    duplicates = df['extracted_cedula'].value_counts()
    duplicates = duplicates[duplicates > 1]
    
    # Registro completo de cada cédula que está duplicada
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
    file_path = "../pcd_0411.csv"  # Replace with your file path
    duplicates, duplicate_records, output_file = find_duplicate_cedulas(file_path)
    
    print("\nDuplicate cédulas found:")
    if len(duplicates) > 0:
        print(duplicates)
        print(f"\nNumber of duplicate records: {len(duplicate_records)}")
    else:
        print("No duplicate cédulas found")
    
    print(f"\nTotal records processed: {len(duplicate_records)}")