import pandas as pd
import os
import time
from datetime import datetime

path = "C:/Users/jyots/Downloads/intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                'Ticker',
                                'DE Ratio',
                                'Price',
                                'SP500'])

    sp500_df = pd.read_csv("$spx_daily_historical-data-01-12-2020.csv")

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        if(len(each_file) > 0):
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                filepath = each_dir + '/' + file
                source = open(filepath, 'r').read().replace('\n', '')

                try:
                    if(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0] == 'N/A'):
                        value = None
                    else:
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%m/%d/%y')
                        row = sp500_df[sp500_df['Time'] == sp500_date]
                        sp500_value = float(row["Last"])
                    except:                                                                                 #Used to compensate for weekends
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%m/%d/%y')
                        row = sp500_df[sp500_df["Time"] == sp500_date]
                        sp500_value = float(row["Last"])

                    #This chunk to find stock_price reliably
                    if source.find('<span id="yfs_l10_aapl">') >= 0:
                        stock_price_string = source.split('<span id="yfs_l10_aapl">')[1].split('</span')[0].replace(',', '')
                    elif source.find('</small><big><b>') >= 0:
                        stock_price_string = source.split('</small><big><b>')[1].split('</b></big>')[0].replace(',', '')
                        if stock_price_string.startswith('<'):
                            stock_price_string = stock_price_string.split('">')[1].split('</span')[0]
                    elif source.find('<span id="yfs_l10_aapl">') >= 0:
                        stock_price_string = source.split('<span id="yfs_l84_aapl">')[1].split('</span')[0].replace(',', '')
                    stock_price = float(stock_price_string)

                    df = df.append({'Date': date_stamp,
                                    'Unix': unix_time,
                                    'Ticker': ticker,
                                    'DE Ratio': value,
                                    'Price': stock_price,
                                    'SP500': sp500_value}, ignore_index = True)
                except Exception as e:
                    pass

            # time.sleep(15)

    save = gather.replace(' ', '').replace('(', '').replace(')', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv(save)

Key_Stats()