import pandas as pd

# Load the CSV file
file_path = "clean_pcd_data.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Randomly sample 300 rows
sampled_data = data.sample(n=200, random_state=42)  # `random_state` ensures reproducibility

# Save the sampled data to a new CSV file
output_path = "sampled_file.csv"  # Replace with desired output file name
sampled_data.to_csv(output_path, index=False)

print(f"300 random rows have been saved to {output_path}")
