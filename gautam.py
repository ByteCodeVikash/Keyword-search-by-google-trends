import os
import time
import pandas as pd
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
def setup_driver(download_path):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
def fetch_data_for_period(driver, start_date, end_date, country_code, keyword, download_path):
    url = f"https://trends.google.com/trends/explore?date={start_date.strftime('%Y-%m-%d')}%20{end_date.strftime('%Y-%m-%d')}&geo={country_code}&q={keyword}"
    driver.get(url)
    time.sleep(8)  # Wait for page to load
    try:
        download_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".widget-actions-item.export")))
        driver.execute_script("arguments[0].scrollIntoView();", download_button)
        driver.execute_script("window.scrollBy(0, -200);")
        driver.execute_script("arguments[0].click();", download_button)
        print(f"Download initiated for keyword: {keyword}")
    except TimeoutException as e:
        print(f"Error during download for {keyword}: ", e)
def read_adjusted_csv(file_path):
    df = pd.read_csv(file_path, skiprows=2)
    df['Day'] = pd.to_datetime(df['Day'])
    return df
def merge_csv_files(csv_directory, output_file):
    csv_files = csv_directory.glob('multiTimeline*.csv')
    data_frames = [read_adjusted_csv(file) for file in csv_files]
    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.sort_values('Day', inplace=True)
    combined_df['Day'] = combined_df['Day'].dt.strftime('%d/%m/%Y')
    combined_df.rename(columns={combined_df.columns[1]: 'Carbon Capture'}, inplace=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined file saved to: {output_file}")
# Define constants and time periods
base_dir = "/home/gautam/Desktop/CODE/trendsGoogle"
data_dir = f"{base_dir}/data/India"
output_dir = f"{base_dir}/Output/India"
countries = {'India': 'IN'}
# keywords = ['COP 26', 'Glasgow Climate Pact', 'GHE', 'Carbon Capture']
keywords =   ['Climate Resilience', 'CMP 16', 'CMA 3', 'Paris Agreement', 'GHG',
            'Carbon Market', 'COP 27', 'Methane Emission', 'Energy Transition',
            'Renewable Energy', 'Sustainable Development', 'Adaptive Capacity',
            'Carbon Capture and Sequestration', 'Carbon Footprint', 'Climate Change',
            'Conference Of The Parties', 'COP', 'ESG', 'Global Average Temperature',
            'Global Warming', 'Green Bond', 'Green House Gas Emission', 'Greenhouse Effect',
            'Heat Waves', 'INDC', 'Indirect Emissions', 'Intended Nationally Determined Contribution',
            'Intergovernmental Panel on Climate Change', 'IPCC', 'Kyoto Protocol',
            'Ozone Depleting Substance', 'Ozone Layer Depletion', 'Reforestation',
            'Sustainability', 'UNFCCC', 'United Nations Framework Convention on Climate Change']
# Ensure base directories exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
# Main process
for keyword in keywords:
    keyword_data_path = Path(f"{data_dir}/{keyword}")
    keyword_output_path = Path(f"{output_dir}/{keyword}")
    os.makedirs(keyword_data_path, exist_ok=True)
    os.makedirs(keyword_output_path, exist_ok=True)
    output_file = keyword_output_path / f"{keyword.replace(' ', '')}.csv"
    driver = setup_driver(str(keyword_data_path))  # Setup driver with keyword-specific download path
    current_date = datetime(2010, 1, 1)
    end_date = datetime.now()
    while current_date < end_date:
        next_date = min(current_date + relativedelta(months=1), end_date)
        fetch_data_for_period(driver, current_date, next_date - timedelta(days=1), 'IN', keyword, str(keyword_data_path))
        current_date = next_date
    driver.quit()
    merge_csv_files(keyword_data_path, str(output_file))







