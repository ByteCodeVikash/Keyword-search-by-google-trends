import time
import pandas as pd
from pytrends.request import TrendReq

# Pytrends session initialize
pytrend = TrendReq()

# Keywords aur countries list
keywords = ['ESG', 'Global Average Temperature',
            'Global Warming', 'Green Bond', 'Green House Gas Emission', 'Greenhouse Effect',
            'Heat Waves', 'INDC', 'Indirect Emissions', 'Intended Nationally Determined Contribution',
            'Intergovernmental Panel on Climate Change', 'IPCC', 'Kyoto Protocol',
            'Ozone Depleting Substance', 'Ozone Layer Depletion', 'Reforestation',
            'Sustainability', 'UNFCCC', 'United Nations Framework Convention on Climate Change']
countries = {'United States': 'US', 'India': 'IN', 'United Kingdom': 'GB'}

# Timeframe for the data
date_interval = '2010-10-01 2015-03-31'

# Creating an Excel writer object
writer = pd.ExcelWriter('Google_Trends_Data.xlsx', engine='xlsxwriter')

# Generate a date range for the entire timeframe to ensure all dates are covered
all_dates = pd.date_range(start=date_interval.split(' ')[0], end=date_interval.split(' ')[1])

for country_name, country_code in countries.items():
    all_data = pd.DataFrame(index=all_dates)
    for keyword in keywords:
        success = False
        while not success:
            try:
                pytrend.build_payload(kw_list=[keyword], timeframe=date_interval, geo=country_code)
                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels=['isPartial'], axis='columns')
                    all_data[keyword] = data.reindex(all_dates, fill_value=0)[keyword]
                else:
                    all_data[keyword] = 0
                success = True
            except Exception as e:
                print("Error with", keyword, "in", country_name, "->", str(e))
                print("Pausing for 60 seconds...")
                time.sleep(60)  # Adjust the pause time as needed
        time.sleep(10)  # Delay to prevent rate limiting

    # Reset index to get the date column, then rename it
    all_data.reset_index(inplace=True)
    all_data.rename(columns={'index': 'Date'}, inplace=True)
    all_data.to_excel(writer, sheet_name=country_name, index=False)

# Save the Excel file
writer.save()
print("Data has been successfully saved to Excel.")
