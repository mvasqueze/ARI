import pandas as pd
from datetime import datetime
import os

def parse_date(date_str):
    """
    Try multiple date formats to parse the date string
    """
    if pd.isna(date_str):
        return None
        
    formats = [
        '%d/%m/%Y %H:%M:%S',     # 08/01/2024 20:54:33
        '%d/%m/%Y %H:%M:%S.%f',  # 08/01/2024 20:54:33.000
        '%Y-%m-%d %H:%M:%S'      # 2024-01-08 20:54:33
    ]
    
    for date_format in formats:
        try:
            return pd.to_datetime(date_str, format=date_format)
        except:
            continue
    return None

def clean_duplicates(file_path):
    try:
        # Read the file with semicolon separator
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        print("Flag1: File successfully read")
        
        # Convert dates using the custom parser
        try:
            df['EditDate'] = df['EditDate'].apply(parse_date)
            print("Flag2: Date conversion completed")
            
            # Check for any NaT values after conversion
            nat_count = df['EditDate'].isna().sum()
            if nat_count > 0:
                print(f"\nWarning: {nat_count} rows had invalid dates")
                # Print some examples of invalid dates
                invalid_dates = df[df['EditDate'].isna()]['EditDate']
                if not invalid_dates.empty:
                    print("\nSample of invalid dates:")
                    print(invalid_dates.head())
                    print("\nSample of original dates that failed conversion:")
                    print(df[df['EditDate'].isna()]['EditDate'].head())
                
                # Remove rows with invalid dates
                df = df.dropna(subset=['EditDate'])
                print(f"Removed {nat_count} rows with invalid dates")
        except Exception as date_error:
            print(f"Error converting dates: {date_error}")
            print("\nSample of dates before conversion:")
            print(df['EditDate'].head())
            raise
        
        # Sort and remove duplicates
        df_cleaned = df.sort_values('EditDate', ascending=False).drop_duplicates(
            subset=['Número de documento (PcD)'],
            keep='first'
        )
        
        # Sort by ObjectID
        if 'ObjectID' in df_cleaned.columns:
            df_cleaned = df_cleaned.sort_values('ObjectID')
        
        # Create output path
        output_path = file_path.rsplit('.', 1)[0] + '_cleaned.' + file_path.rsplit('.', 1)[1]
        
        # Save cleaned dataset
        df_cleaned.to_csv(output_path, sep=';', index=False)
        
        # Generate summary
        total_initial = len(df)
        total_final = len(df_cleaned)
        duplicates_removed = total_initial - total_final
        
        print("\nCleaning Summary:")
        print(f"Initial records: {total_initial}")
        print(f"Records after cleaning: {total_final}")
        print(f"Duplicates removed: {duplicates_removed}")
        
        return df_cleaned
        
    except pd.errors.EmptyDataError:
        print("The file is empty")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        # Print more detailed error information
        import traceback
        print("\nDetailed error information:")
        print(traceback.format_exc())
        return None

def main():
    file_path = "../pcd-3.csv"
    
    try:
        print(f"Processing file: {file_path}")
        duplicados = clean_duplicates(file_path)
        
        if duplicados is not None:
            print("\nProcessing completed successfully")
            # Print sample of processed dates
            if 'EditDate' in duplicados.columns:
                print("\nSample of processed dates:")
                print(duplicados['EditDate'].head())
        else:
            print("\nProcessing failed")
            
    except Exception as e:
        print(f"Auxilio! Algo pasó: {e}")

if __name__ == "__main__":
    main()