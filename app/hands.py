import os
import tushare as ts
from datetime import datetime
from datetime import timedelta
import time
import matplotlib.pyplot as plt
from operate import fetch
import pandas as pd


def getdir(code):
    path = "/home/ee/data/" + code
    if os.path.isdir(path) is False:
        os.mkdir(path)
    return path


def savek(code, day, replace=False):
    print(day, code)
    dirpath = getdir(code)
    path = "{0}/ticks_{1}_{2}.png".format(dirpath, code, day)
    if replace is False and os.path.isfile(path) is True:
        print("{0} already exists.".format(path))
        return
    print(path)
    df = ts.get_tick_data(code, day)
    pivot = fetch.Fetch.get_pivot(code, day)
    if df is None or len(df) == 0 or pivot <= 0:
        return

    df = df.reindex(index=df.index[::-1])
    df['ratio'] = (df['price'] - pivot) / pivot
    max_ratio = df.iloc[:, 6].dropna().max()
    min_ratio = df.iloc[:, 6].dropna().min()
    if max_ratio < 0.05:
        max_ratio = 0.05
    if min_ratio > -0.05:
        min_ratio = -0.05

    print(df.head(10))
    df.plot(x='time', y='ratio')
    plt.ylim([min_ratio, max_ratio])
    for i in range(0, 41):
        y = -0.1 + 0.005 * i
        if y >= min_ratio and y <= max_ratio:
            if i % 2 == 0:
                plt.axhline(y, ls='-', color='red')
            else:
                plt.axhline(y, ls='--')

    plt.axhline(0, ls='-', color='black')
    plt.axvline(len(df.index) / 8, color='red')
    plt.axvline(len(df.index) / 4, color='red')
    plt.axvline(len(df.index) / 8 * 3, color='red')
    plt.axvline(len(df.index) / 2, color='red')
    plt.axvline(len(df.index) / 8 * 7, color='red')
    # plt.show()
    plt.savefig(path, dpi=420)
    plt.close()
    #time.sleep(1)

    print('finish')

def batch_savek():
    codes = ['601318', '600036', '601601', '002415']
    # codes = []
    start = '2017-8-1'
    end = '2017-8-29'
    for code in codes:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        while start_date <= end_date:
            day = start_date.strftime('%Y-%m-%d')
            start_date = start_date + timedelta(days=1)

            while True:
                try:
                    savek(code, day)
                    time.sleep(3)
                except IOError:
                    print("waiting {0} seconds to try again".format(10))
                    time.sleep(10)
                    continue
                break


def batch_save_hist():
    df = ts.get_stock_basics('2017-09-01')
    codes = df.index
    #codes = ['601318', '600036', '601601', '002415', '600988', '002508', '000651']
    start = '2016-8-1'
    end = '2017-8-29'
    for code in codes:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        while start_date <= end_date:
            day = start_date.strftime('%Y-%m-%d')
            start_date = start_date + timedelta(days=1)
            print("[{0} {1}]".format(code, day))
            while True:
                try:
                    fetch.Fetch.get_pivot(code, day, day)
                    time.sleep(3)
                    fetch.Fetch.get_hist_tick(code, day)
                except IOError:
                    print("waiting {0} seconds to try again".format(10))
                    time.sleep(10)
                    continue
                break


def batch_save_group():
    codes = ['601318', '600036', '601601', '002415']
    start = '2016-8-1'
    end = '2017-8-29'
    for code in codes:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        while start_date <= end_date:
            day = start_date.strftime('%Y-%m-%d')
            start_date = start_date + timedelta(days=1)

            while True:
                try:
                    fetch.Fetch.get_price_group(code, day)
                    time.sleep(1)
                except IOError:
                    print("waiting {0} seconds to try again".format(10))
                    time.sleep(10)
                    continue
                break


def show_group(code, start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    df = pd.DataFrame()
    while start_date <= end_date:
        day = start_date.strftime('%Y-%m-%d')
        start_date = start_date + timedelta(days=1)

        while True:
            try:
                t = fetch.Fetch.get_price_group(code, day)
                if len(df.index) == 0:
                    df = t
                else:
                    df = df.append(t)
                #print(len(df.index))
                #time.sleep(1)
            except IOError:
                print("waiting {0} seconds to try again".format(10))
                time.sleep(10)
                continue
            break

    if df is None:
        return

    df = df.groupby('price').sum()
    df['ratio'] = df['volume']
    prev = None
    total = 0
    for i in df.index:
        total += df.loc[i, 'volume']
        df.loc[i, 'ratio'] = total

    if total > 0:
        for i in df.index:
            df.loc[i, 'ratio'] = df.loc[i, 'ratio'] / total

    #print(df)
    fig = plt.figure()
    hvol = fig.add_subplot(121)
    hrat = fig.add_subplot(122)
    hvol.hlines(df.index, [0], df['volume'])
    hrat.plot(df['ratio'], df.index, '^')
    #hrat.hlines(df.index, [0], df['ratio'])
    plt.show()

if __name__ == "__main__":
    batch_save_hist()
    #batch_savek()
    #batch_save_group()
    #show_group('601318', '2017-3-15', '2017-5-1')



