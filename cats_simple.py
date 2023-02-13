# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import date, timedelta

df = pd.DataFrame()
flag_mode_startend = False
time_stamp_start = date

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

    if event.dblclick:
        timestamp = matplotlib.dates.num2date(event.xdata).strftime('%Y-%m-%d %H:%M:%S')
        print(timestamp)
        # print(df[1:2])

        if df["temp_s3"][timestamp] is not None:
            print(df["temp_s3"][timestamp])

        global flag_mode_startend
        global time_stamp_start

        print(df.head(6))

        if flag_mode_startend == False:
            flag_mode_startend = True
            print(" from here ")
            time_stamp_start = timestamp
        else:
            flag_mode_startend = False

            # 対象データを書き換え
            df.loc[time_stamp_start:timestamp,"phase"] = 1
            ax2.fill_between(df.index, df["phase"],fc="green", alpha=0.2)

            print(" until here ")

        # csv_data = pd.read_csv(file_name,header=0,parse_dates=["date"])

def plot_and_show():
    pass


if __name__ == '__main__':
    print('getcwd:      ', os.getcwd())
    print('__file__:    ', __file__)

    paths = pathlib.Path('./')   
    temprature_files = paths.glob('*.csv')
    list_gen = list(temprature_files)

    file_name = list_gen[0]
    print(file_name)

    # Figureを作成
    Figure, axis = plt.subplots(1,1,figsize=(16,4), tight_layout=True)
    # axis = Figure.add_subplot(1,1,1) # axを持っておく

    if True:
        try:
            csv_data = pd.read_csv("desc/"+str(file_name),header=0,parse_dates=["date"])

            csv_data.set_index('date',inplace=True)

            # 既にAnotation済み？phase列
            if not 'phase' in csv_data.columns :
                print('まだAnotationしていない状態のため、training data用のcolumnを追加')
                # 列を追加し、fill by 0
                csv_data['phase'] = 0

            # data 加工部
            # global df
            df = csv_data

            axis.set_xlabel("time")
            axis.set_ylabel("temp")
            axis.set_ylim(80,100)

            axis.plot(csv_data.index, csv_data["temp_s1"],"r-", alpha=0.6, label="temp_s1",marker=".")
            axis.plot(csv_data.index, csv_data["temp_s3"],"b-", alpha=0.6, label="temp_s3",marker=".")

            ax2 = axis.twinx()
            ax2.fill_between(csv_data.index, csv_data["phase"],fc="green", alpha=0.2)

            cid = Figure.canvas.mpl_connect('button_press_event', onclick)

            plt.title(file_name.stem)
            plt.grid()
            plt.show()
            # plt.savefig('desc/'+ file_name.stem +'.png')

            #
            # データ出力
            #
            csv_data.to_csv('desc/'+ file_name.stem +'.csv')

        except Exception as e:
            print(e)