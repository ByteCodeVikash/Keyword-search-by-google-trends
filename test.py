import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the Selenium WebDriver
try:
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disable unnecessary logs
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    options = webdriver.ChromeOptions()
    options.add_argument('--enable-logging')
    options.add_argument('--v=1')
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print(f"Exception occurred: {e}")
    raise

# List of countries and their Google Trends region codes
countries = {
    'United States': 'US', 
}

# Keywords to search
keywords = ['COP 26', ]

# Create a dictionary for DataFrames
data = {country: pd.DataFrame(index=pd.date_range(start="2022-01-01", end="2022-03-31", freq='D')) for country in countries}

# Function to fetch Google Trends data
def fetch_google_trends_data(driver, country, keyword):
    # Generate the Google Trends URL
    url = f"https://trends.google.com/trends/explore?date=2022-01-01%2022-03-3&geo={countries[country]}&q={keyword}"
    driver.get(url)
    
    # Use WebDriverWait to wait for specific elements to load
    try:
        # Wait for the specific element to load
        chart_presence = EC.presence_of_element_located((By.CSS_SELECTOR, "div.widget-template"))
        WebDriverWait(driver, 30).until(chart_presence)
        
        # Extract data from the chart
        chart_element = driver.find_element(By.CSS_SELECTOR, "div.widget-template")
        extracted_data = chart_element.text  # Modify this to match your data extraction logic
        
        return extracted_data
    
    except Exception as e:
        print(f"Error fetching data for {country} - {keyword}: {str(e)}")
        return 0  # Return zero if there's an error or no data found

# Loop through countries and keywords to gather data
for country in countries:
    for keyword in keywords:
        print(f"Fetching data for {country} - {keyword}")
        for date in data[country].index:
            result = fetch_google_trends_data(driver, country, keyword)
            try:
                result = float(result)  # Convert to float if possible
            except ValueError:
                result = 0  # Default to zero if conversion fails
            
            # Store the result in the DataFrame
            data[country].loc[date, keyword] = result

# Save the data to Excel and print confirmation or error
try:
    with pd.ExcelWriter('Google_Trends_Data.xlsx') as writer:
        for country in data:
            data[country].to_excel(writer, sheet_name=country)
    
    print("Data saved successfully to 'Google_Trends_Data.xlsx'.")
except Exception as e:
    print(f"Error saving data to Excel: {str(e)}")


from selenium.common.exceptions import TimeoutException

# Function to fetch Google Trends data with explicit waits and detailed console output
def fetch_google_trends_data(driver, country, keyword, date):
    # Generate the URL for the keyword and country
    url = f"https://trends.google.com/trends/explore?date={date:%Y-%m-%d} {date:%Y-%m-%d}&geo={countries[country]}&q={keyword}"
    
    # Attempt to open the URL
    try:
        driver.get(url)
        print(f"Accessing URL for {keyword} in {country} on {date.date()}")
    except Exception as e:
        print(f"Failed to open URL for {keyword} in {country} on {date.date()}: {e}")
        return None

    # Use WebDriverWait to wait for the chart element
    try:
        # Specify the chart element's CSS selector
        chart_selector = "div.widget-template"  # Replace with actual selector
        chart_presence = EC.presence_of_element_located((By.CSS_SELECTOR, chart_selector))
        
        # Wait for the chart to be present, timeout after 30 seconds
        WebDriverWait(driver, 30).until(chart_presence)
        print(f"Chart element found for {keyword} in {country} on {date.date()}")

        # Extract data from the chart element
        chart_element = driver.find_element(By.CSS_SELECTOR, chart_selector)
        data = chart_element.text  # This is an example; you'll need to adjust extraction logic
        
        print(f"Data extracted for {keyword} in {country} on {date.date()}: {data}")
        return data

    except TimeoutException:
        print(f"Loading timeout for {keyword} in {country} on {date.date()}")
        return 0
    except Exception as e:
        print(f"Error extracting data for {keyword} in {country} on {date.date()}: {e}")
        return 0

# Loop through countries and keywords to populate data
for country in countries:
    for keyword in keywords:
        print(f"Starting data fetch for {country} - {keyword}")
        
        for date in data[country].index:
            result = fetch_google_trends_data(driver, country, keyword, date)
            data[country].at[date, keyword] = result if result is not None else 0

            if result is not None:
                print(f"Data saved for {keyword} on {date.date()}: {result}")
            else:
                print(f"No data available for {keyword} on {date.date()}, saved as 0")

# Function to download data
def download_google_trends_data(driver, country, keyword):
    # Generate the URL for the keyword and country
    url = f"https://trends.google.com/trends/explore?date=2022-01-01%2022-02-3&geo={countries[country]}&q={keyword}"
    driver.get(url)
    
    try:
        # Wait for the chart element to be present
        chart_selector = "div.widget-template"  # Update this selector if needed
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, chart_selector)))
        
        # Click on the download button
        download_button_selector = 'div.widget-actions-menu button[aria-label="Download"]'
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, download_button_selector)))
        download_button = driver.find_element(By.CSS_SELECTOR, download_button_selector)
        download_button.click()

        # Wait for the download to finish
        # You may want to implement a more robust file download check
        time.sleep(10)  # Adjust time as needed

    except TimeoutException as e:
        print(f"Loading timeout for {keyword} in {country}")
        return False
    except Exception as e:
        print(f"Error downloading data for {keyword} in {country}: {e}")
        return False
    return True

# Loop through countries and keywords to download data
for country in countries:
    for keyword in keywords:
        print(f"Downloading data for {country} - {keyword}")
        success = download_google_trends_data(driver, country, keyword)
        if success:
            print(f"Data downloaded for {keyword} in {country}")
        else:
            print(f"Failed to download data for {keyword} in {country}")

# Close the Selenium WebDriver
driver.quit()

















