import pandas as pd
import os
import pathlib
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import date, timedelta

df = pd.DataFrame()

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    timestamp = matplotlib.dates.num2date(event.xdata).strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp)
    # print(df[1:2])
    print(df["temp_s3"][timestamp])
    df.at[timestamp,"mov_separator"] = 1

# def get_daily_chart(_date:date):
def get_daily_chart(file_name):
    #
    # データ読み込み
    #
    print(file_name)
    csv_data = pd.read_csv(file_name,header=0,parse_dates=["date"])
    # date,temp_s1,temp_s3,cooking,mov_separator,phase1,phase2,phase3,phase4,phase5,phase6,phase7,phase8,phase9
    # 2022/3/2 13:26:45,90.92,90.47,0,0,0,0,0,0,0,0,0,0,0
    # 2022/3/2 13:26:46,91.20571367,90.57173456,0,0,0,0,0,0,0,0,0,0,0

    csv_data.set_index('date',inplace=True)

    # 既にAnotation済み？cooking列
    if not 'cooking' in csv_data.columns :
        print('まだAnotationしていない状態のため、training data用のcolumnを追加')
        # 列を追加し、fill by 0
        csv_data['cooking'] = 0
        csv_data['mov_separator'] = 0
        csv_data['phase1'] = 0
        csv_data['phase2'] = 0
        csv_data['phase3'] = 0
        csv_data['phase4'] = 0
        csv_data['phase5'] = 0
        csv_data['phase6'] = 0
        csv_data['phase7'] = 0
        csv_data['phase8'] = 0
        csv_data['phase9'] = 0

    # data 加工部
    global df
    df = csv_data
    print("----------")
    print(df[1:2])

    #
    # データ描画部
    #
    fig, ax1 = plt.subplots(1,1,figsize=(16,4), tight_layout=True)

    if True:
        try:
            ax1.set_xlabel("time")
            ax1.set_ylabel("temp")
            ax1.set_ylim(80,100)

            ax1.plot(csv_data.index, csv_data["temp_s1"],"r-", alpha=0.6, label="temp_s1",marker=".")
            ax1.plot(csv_data.index, csv_data["temp_s3"],"b-", alpha=0.6, label="temp_s3",marker=".")

            ax2 = ax1.twinx()
            ax2.fill_between(csv_data.index, csv_data["mov_separator"],fc="green", alpha=0.2)

            cid = fig.canvas.mpl_connect('button_press_event', onclick)

            plt.title(file_name.stem)
            plt.grid()
            plt.show()
            plt.savefig('desc/'+ file_name.stem +'.png')
        except Exception as e:
            print(e)

        # Export to CSV
        csv_data.to_csv('desc/'+ file_name.stem +'.csv')
        print("export to "+'desc/'+ file_name.stem +'.csv')

def date_range(start, stop, step = timedelta(days=1)):
    current = start
    while current < stop:
        yield current
        current += step

if __name__ == '__main__':
    print('getcwd:      ', os.getcwd())
    print('__file__:    ', __file__)

    # 指定した日付の期間をループで回す
    # for d in date_range(date(2022, 4, 19), date(2022, 5, 17+1)):
    #     print(d.strftime('%Y%m%d'))
    paths = pathlib.Path('./')
    
    temprature_files = paths.glob('*.csv')
    
    # 読み込むファイルのリストを走査
    for file in temprature_files:
        get_daily_chart(file)