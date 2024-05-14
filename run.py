import os
import pandas as pd
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq
from pathlib import Path
def fetch_data_for_period(py_trends, start_date, end_date, country_code, keyword, output_path):
    # Set the timeframe for the data request
    timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
    # Set the geo location for the data request
    attempts = 0
    while attempts < 5:
        try:
            py_trends.build_payload([keyword], timeframe=timeframe, geo=country_code)
            data = py_trends.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'], axis=1, errors='ignore')
                data.to_csv(output_path / f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_{keyword.replace(' ', '')}.csv")
                print(f"Data downloaded for keyword: {keyword}, from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            return
        except Exception as e:
            print(f"Error retrieving data for {keyword}, attempt {attempts+1}: {e}")
            time.sleep((2 ** attempts) * 60)  # Exponential backoff
            attempts += 1
    print(f"Failed to retrieve data for {keyword} after several attempts.")
def read_adjusted_csv(file_path):
    df = pd.read_csv(file_path)
    if 'date' not in df.columns:
        date_column = df.columns[0]
    else:
        date_column = 'date'
    df[date_column] = pd.to_datetime(df[date_column]).dt.strftime('%d/%m/%Y')
    df.rename(columns={date_column: 'date'}, inplace=True)
    return df
def merge_csv_files(csv_directory, output_file):
    csv_files = csv_directory.glob('*.csv')
    data_frames = [read_adjusted_csv(file) for file in csv_files]
    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.sort_values('date', inplace=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined file saved to: {output_file}")
py_trends = TrendReq(hl='en-US', tz=360)
base_dir = r"C:\Users\Vikash\OneDrive\Desktop\gtrandes\gautam"
data_dir = Path(f"{base_dir}/data/India")
output_dir = Path(f"{base_dir}/Output/India")
countries = {'United States': 'US'}
keywords = ['Climate Resilience', 'CMP 16', 'CMA 3', 'Paris Agreement', 'GHG',]
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
for keyword in keywords:
    keyword_data_path = data_dir / keyword
    keyword_output_path = output_dir / keyword
    os.makedirs(keyword_data_path, exist_ok=True)
    os.makedirs(keyword_output_path, exist_ok=True)
    output_file = keyword_output_path / f"{keyword.replace(' ', '')}.csv"
    current_date = datetime(2010, 1, 1)
    end_date = datetime.now()
    while current_date < end_date:
        next_date = min(current_date + relativedelta(months=1), end_date)
        fetch_data_for_period(py_trends, current_date, next_date - relativedelta(days=1), 'IN', keyword, keyword_data_path)
        current_date = next_date
    merge_csv_files(keyword_data_path, str(output_file))









