import pandas as pd
import os
import time
from datetime import datetime

path = "C:/Users/jyots/Downloads/intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE Ratio'])

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
                    df = df.append({'Date': date_stamp, 'Unix': unix_time, 'Ticker': ticker, "DE Ratio": value}, ignore_index = True)
                except Exception as e:
                    pass

            # time.sleep(15)

    save = gather.replace(' ', '').replace('(', '').replace(')', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv(save)

Key_Stats()