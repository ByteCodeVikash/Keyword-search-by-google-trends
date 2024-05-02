import json
import openpyxl

# Given JSON data
json_data = '''
{
    "default": {
        "rankedList": [
            {
                "rankedKeyword": [
                    {
                        "query": "cop 27",
                        "value": 100,
                        "formattedValue": "100",
                        "hasData": true,
                        "link": "/trends/explore?q=cop+27&date=2023-01-01+2023-12-31&geo=US"
                    },
                    {
                        "query": "cop 28",
                        "value": 80,
                        "formattedValue": "80",
                        "hasData": true,
                        "link": "/trends/explore?q=cop+28&date=2023-01-01+2023-12-31&geo=US"
                    },
                    {
                        "query": "cop 26 glasgow",
                        "value": 64,
                        "formattedValue": "64",
                        "hasData": true,
                        "link": "/trends/explore?q=cop+26+glasgow&date=2023-01-01+2023-12-31&geo=US"
                    },
                    {
                        "query": "cop 21",
                        "value": 35,
                        "formattedValue": "35",
                        "hasData": true,
                        "link": "/trends/explore?q=cop+21&date=2023-01-01+2023-12-31&geo=US"
                    },
                    {
                        "query": "cop 25",
                        "value": 13,
                        "formattedValue": "13",
                        "hasData": true,
                        "link": "/trends/explore?q=cop+25&date=2023-01-01+2023-12-31&geo=US"
                    }
                ]
            },
            {
                "rankedKeyword": [
                    {
                        "query": "cop 28",
                        "value": 750,
                        "formattedValue": "+750%",
                        "link": "/trends/explore?q=cop+28&date=2023-01-01+2023-12-31&geo=US"
                    },
                    {
                        "query": "cop 21",
                        "value": 150,
                        "formattedValue": "+150%",
                        "link": "/trends/explore?q=cop+21&date=2023-01-01+2023-12-31&geo=US"
                    }
                ]
            }
        ]
    }
}
'''

# Convert JSON string to Python dictionary
data_dict = json.loads(json_data)

# Create a new Excel workbook
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'Search Volume Data'

# Add header row to the Excel sheet
sheet.append(['Keyword', 'Search Volume', 'Formatted Search Volume', 'Link'])

# Extract data and enter into the sheet
for ranked_list in data_dict['default']['rankedList']:
    for keyword_info in ranked_list['rankedKeyword']:
        # Prepare row data for each keyword
        row_data = [
            keyword_info['query'],
            keyword_info['value'],
            keyword_info['formattedValue'],
            'https://trends.google.com' + keyword_info['link']
        ]
        # Append row data to the sheet
        sheet.append(row_data)

# Save the workbook
wb.save('Google_Trends_Search_Volume.xlsx')
