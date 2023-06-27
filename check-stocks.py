import mechanicalsoup
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

browser = mechanicalsoup.StatefulBrowser()


url = "https://www.magicformulainvesting.com/Screening/StockScreening"
browser.open(url)

# login
browser.select_form()

# browser.get_current_form().print_summary()
browser["Email"] = os.environ.get("EMAIL")
browser["Password"] = os.environ.get("PASSWORD")
browser.submit_selected()

# select correct radio button
browser.select_form()
browser["Select30"] = "false"
browser.submit_selected()

# get the table
table_div = browser.page.find('div', {'id': 'tableform' })
table = table_div.find('table')
magic_stocks_data_frame = pd.read_html(str(table))[0]

url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=180&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&excludeDerivRelated=1&vl=20&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&iscob=1&isceo=1&ispres=1&iscfo=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1"
browser.open(url)

table = browser.page.find('table', {'class': 'tinytable'})
open_insider_data_frame = pd.read_html(str(table))[0]


# compare the two data frames
merged_data_frame = pd.merge(magic_stocks_data_frame, open_insider_data_frame, on=['Ticker'], how='inner')

if len(merged_data_frame) > 0:
    print("There are some stocks that are in both lists")
    print(merged_data_frame)
