import pandas as pd
import os
import time
from datetime import datetime

path = "C:/Users/jyots/Downloads/intraQuarter"

def Key_Stats(gather="Total Debt/Equit (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    # print(stock_list)

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        if(len(each_file) > 0):
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                print(date_stamp, unix_time)
                time.sleep(15)

Key_Stats()