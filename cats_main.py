# -*- coding: utf-8 -*-

import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import date, timedelta

df = pd.DataFrame()

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    timestamp = matplotlib.dates.num2date(event.xdata).strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp)
    # print(df[1:2])
    if df["temp_s3"][timestamp] is not None:
        print(df["temp_s3"][timestamp])
    df.at[timestamp,"mov_separator"] = 1

def date_range(start, stop, step = timedelta(days=1)):
    current = start
    while current < stop:
        yield current
        current += step

class Test(QtWidgets.QDialog):
    def __init__(self,file_name, parent=None):
        super(Test, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        # リスト作成
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode( #複数選択可能にする
            QtWidgets.QAbstractItemView.MultiSelection
        )
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 211, 291))
        for i in range(10):
            item = QtWidgets.QListWidgetItem("%i" % i)
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.printItemText)

        # Figureを作成
        self.Figure, self.axis = plt.subplots(1,1,figsize=(16,4), tight_layout=True)
        self.FigureCanvas = FigureCanvas(self.Figure)  # FigureをFigureCanvasに追加
        # self.axis = self.Figure.add_subplot(1,1,1) # axを持っておく

        if True:
            try:
                csv_data = pd.read_csv(file_name,header=0,parse_dates=["date"])

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

                self.axis.set_xlabel("time")
                self.axis.set_ylabel("temp")
                self.axis.set_ylim(80,100)

                self.axis.plot(csv_data.index, csv_data["temp_s1"],"r-", alpha=0.6, label="temp_s1",marker=".")
                self.axis.plot(csv_data.index, csv_data["temp_s3"],"b-", alpha=0.6, label="temp_s3",marker=".")

                ax2 = self.axis.twinx()
                ax2.fill_between(csv_data.index, csv_data["mov_separator"],fc="green", alpha=0.2)

                cid = self.Figure.canvas.mpl_connect('button_press_event', onclick)

                # plt.title(file_name.stem)
                # plt.grid()
                # plt.show()
                # plt.savefig('desc/'+ file_name.stem +'.png')
            except Exception as e:
                print(e)
            
        self.layout.addWidget(self.add_label("Ctrlを押しながらで複数選択"))
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.FigureCanvas)
        self.setLayout(self.layout)


    def add_label(self,text):
        # ラベルを作る
        label1=QtWidgets.QLabel(self)
        label1.setText(text)
        label1.adjustSize()
        return label1


    def printItemText(self):
        # 選択したアイテムを表示
        items = self.listWidget.selectedItems()
        x = []
        for i in range(len(items)):
            x.append(int(self.listWidget.selectedItems()[i].text()))

        print(x)
        self.update_Figure(x)

    # Figure
    def update_Figure(self,x):
        self.axis.cla() # リセットを掛ける必要がある。
        self.axis.plot(x,'-o')
        plt.grid(); plt.legend(["selected number"])
        self.FigureCanvas.draw()

if __name__ == '__main__':
    print('getcwd:      ', os.getcwd())
    print('__file__:    ', __file__)

    paths = pathlib.Path('./')   
    temprature_files = paths.glob('*.csv')
    list_gen = list(temprature_files)
    print(list_gen[0])

    # get_daily_chart(list_gen[0])

    app = QtWidgets.QApplication(sys.argv)

    form = Test(file_name=list_gen[0])
    form.show()
    sys.exit(app.exec_())