import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

import re

path = "C:/Users/jyots/Downloads/intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                'Ticker',
                                'DE Ratio',
                                'Price',
                                'Stock Price Change',
                                'SP500',
                                'SP500 Change',
                                'Difference'])

    sp500_df = pd.read_csv("$spx_daily_historical-data-01-12-2020.csv")

    ticker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if(len(each_file) > 0):
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                filepath = each_dir + '/' + file
                source = open(filepath, 'r').read().replace('\n', '')

                try:
                    try:
                        if (source.find(gather + ':</td><td class="yfnc_tabledata1">N/A</td>')) or (source.find(gather + ':</th><td class="yfnc_tabledata1">N/A</td>')):
                            value = None
                        elif source.find(gather + ':</td><td class="yfnc_tabledata1">') > 0:
                            value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0].replace(',', ''))
                        elif source.find(gather + ':</th><td class="yfnc_tabledata1">') > 0:
                            value = float(source.split(gather + ':</th><td class="yfnc_tabledata1">')[1].split('</td>')[0].replace(',', ''))
                    except Exception as e:
                        print("BLASFBLFADJBG", str(e), ticker, filepath)
                    
                    sp500_date = datetime.fromtimestamp(unix_time).strftime('%m/%d/%y')
                    for x in range(1, 7):
                        try:
                            row = sp500_df[sp500_df['Time'] == sp500_date]
                            sp500_value = float(row["Last"])
                        except Exception as e:
                            pass
                        sp500_date = datetime.fromtimestamp(unix_time - x * 86400).strftime('%m/%d/%y')
                        if isinstance(sp500_value, float):
                            break

                    #This chunk to find stock_price reliably
                    if source.find('</small><big><b>') >= 0:
                        stock_price_string = source.split('</small><big><b>')[1].split('</b></big>')[0].replace(',', '')
                        stock_price_string = re.search(r'(\d{1,8}\.\d{1,8})', stock_price_string).group(1)
                    elif source.find('<span class="time_rtq_ticker">') >= 0:
                        stock_price_string = source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0].replace(',', '')
                        stock_price_string = re.search(r'(\d{1,8}\.\d{1,8})', stock_price_string).group(1)
                    stock_price = float(stock_price_string)

                    if not starting_stock_value and isinstance(stock_price, float):
                        starting_stock_value = stock_price
                    if not starting_sp500_value and isinstance(sp500_value, float):
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    df = df.append({'Date': date_stamp,
                                    'Unix': unix_time,
                                    'Ticker': ticker,
                                    'DE Ratio': value,
                                    'Price': stock_price,
                                    'Stock Price Change': stock_p_change,
                                    'SP500': sp500_value,
                                    'SP500 Change': sp500_change,
                                    'Difference': stock_p_change - sp500_change}, ignore_index = True)
                except Exception as e:
                    print(str(e), ticker, filepath)

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])

            plot_df['Difference'].plot(label = each_ticker)
            plt.legend()

        except Exception as e:
            pass

    plt.show()

    save = gather.replace(' ', '').replace('(', '').replace(')', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv(save)

Key_Stats()