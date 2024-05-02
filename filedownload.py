import os
import time
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
def fetch_data_for_period(driver, start_date, end_date, country_code, keyword):
    url = f"https://trends.google.com/trends/explore?date={start_date.strftime('%Y-%m-%d')}%20{end_date.strftime('%Y-%m-%d')}&geo={country_code}&q={keyword}"
    driver.get(url)
    time.sleep(5)  # Wait for page to load
    try:
        download_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".widget-actions-item.export")))
        driver.execute_script("arguments[0].scrollIntoView();", download_button)
        driver.execute_script("window.scrollBy(0, -200);")
        driver.execute_script("arguments[0].click();", download_button)
        print("Download initiated for keyword:", keyword)
    except TimeoutException as e:
        print("Error during download: ", e)
def merge_dataframes(download_path, output_file):
    all_files = [os.path.join(download_path, f) for f in os.listdir(download_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(file) for file in all_files]
    full_df = pd.concat(df_list)
    full_df.to_csv(output_file, index=False)
    print("Data merged and saved to", output_file)
# Define constants and time periods
countries = {'United States': 'US'}
keywords = ['COP 26']  # Add your keywords here
start_date = datetime(2010, 1, 1)
end_date = datetime.now()
current_date = start_date
download_path =r"C:\Users\Vikash\OneDrive\Desktop\gtrandes\downloadedfile"
# Main process
os.makedirs(download_path, exist_ok=True)
driver = setup_driver(download_path)
while current_date < end_date:
    #next_date = min(current_date + timedelta(days=5*30), end_date)  # Calculate next 5 months
    next_date = min(current_date + timedelta(days=150), end_date)
    for country, country_code in countries.items():
        for keyword in keywords:
            fetch_data_for_period(driver, current_date, next_date, country_code, keyword)
    current_date = next_date + timedelta(days=1)
driver.quit()
merge_dataframes(download_path, "Final_Google_Trends_Data.csv")