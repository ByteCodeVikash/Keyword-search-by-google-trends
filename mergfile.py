import pandas as pd
from pathlib import Path
def read_adjusted_csv(file_path):
    # Read the CSV file, skipping the first two lines to adjust for header and extra descriptions
    df = pd.read_csv(file_path, skiprows=2)
    # Convert the 'Day' column to datetime to ensure correct sorting
    df['Day'] = pd.to_datetime(df['Day'])
    return df
# Path to the directory containing your CSV files
csv_directory = Path(r'C:\Users\Vikash\OneDrive\Desktop\gtrandes\downloadedfile')
# Find all CSV files in the directory
csv_files = csv_directory.glob('*.csv')
# Read all CSV files using the adjusted function and combine them
data_frames = [read_adjusted_csv(file) for file in csv_files]
combined_df = pd.concat(data_frames, ignore_index=True)
# Sort the DataFrame by the 'Day' column
combined_df.sort_values('Day', inplace=True)
# Convert the 'Day' column to 'DDMMYYYY' format
combined_df['Day'] = combined_df['Day'].dt.strftime('%d/%m/%Y')
# Save the combined DataFrame to a new CSV file
combined_df.to_csv(r'C:\Users\Vikash\OneDrive\Desktop\gtrandes\finaldata\United States\COP 26(COP 26).csv', index=False)
# Example usage of the combined DataFrame
print(combined_df.head())









