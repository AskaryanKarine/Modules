"""The program is to build life-candlestick charts"""

import argparse
import os
from urllib.request import urlopen
import pandas
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_finance import candlestick2_ohlc

def getting_data(nasdaq_code: str):
    """Function for receiving data from the Finam (SBER) and Tiingo (others).
    The function accepts the nasdaq company code.
    Returns a minute-by-minute DataFrame in the OHLC format"""

    if nasdaq_code == 'SBER':
        url = 'http://export.finam.ru/SBER_20190601_20190607.csv?market=0&em=3&code=SBER'+\
              '&apply=0&df=1&mf=5&yf=2019&from=2019-06-01&dt=7&mt=5&yt=2019&to=2019-06-07'+\
                  '&p=2&f=price&e=.csv&cn=SBER&dtf=4&tmf=3&MSOR=0&mstime=on&mstimever=1'+\
                      '&sep=1&sep2=1&datf=1&at=1'
        txt = urlopen(url).readlines()
        with open('temp.csv', "w") as temp_file:
            for line in txt:
                temp_file.write(line.strip().decode("utf-8")+'\n')

        data_frame = pandas.read_csv('temp.csv', names=['TICKER', 'PER', 'DATE', 'TIME', 'open',
                                                        'high', 'low', 'close', 'VOL'])
        data_frame.drop(data_frame.index[0], inplace=True)
        data_frame.reset_index(inplace=True)
        data_frame.insert(0, column='date', value=(data_frame['DATE']+' '+data_frame['TIME']))
        del data_frame['index'], data_frame['DATE'], data_frame['TIME'], data_frame['TICKER']
        del data_frame['PER'], data_frame['VOL']
        data_frame['date'] = pandas.to_datetime(data_frame['date'],
                                                format='%d/%m/%y %H:%M:%S', exact=False)
    else:
        request = requests.get("https://api.tiingo.com/iex/{}/".format(nasdaq_code)+\
                               "prices?startDate=2019-06-01&endDate=2019-06-07&"+\
                               "resampleFreq=1min&token=f4b490cd38"+\
                               "cf0a21bc5ee71dff43781641b3f7b0&format=csv")
        with open('temp.csv', 'w') as temp_file:
            temp_file.write(request.text)
        data_frame = pandas.read_csv('temp.csv')
        del data_frame['volume']
        data_frame['date'] = pandas.to_datetime(data_frame['date'])
        data_frame['date'] = data_frame['date'].dt.strftime('%Y/%m/%d %H:%M:%S')
        data_frame['date'] = pandas.to_datetime(data_frame['date'])

    os.remove('temp.csv')
    return data_frame


def my_ohlc(data_frame, interval):
    """Function for calculating OHLC for a given period of time.
    Returns a DataFrame in OHLC format
    where data_frame -- a minute-by-minute DataFrame in the OHLC format,
          interval -- int, a given period of time"""

    end_day = data_frame.date[0]+pandas.Timedelta(days=1)
    start_day = data_frame.date[0]
    delta = pandas.Timedelta(minutes=interval)
    data_frame_result = pandas.DataFrame()
    while True:
        df_days = data_frame[(data_frame['date'] >= start_day) & (data_frame['date'] < end_day)]
        start_i = start_day
        end_i = start_i+delta
        while True:
            bool2 = (df_days['date'] >= start_i) & (df_days['date'] <= end_i)
            df_min = df_days[bool2]
            if df_min.empty:
                break
            index_close = df_min.date[df_min.date == end_i].index.tolist()
            index_open = df_min.date[df_min.date == start_i].index.tolist()
            if not index_close:
                index_close = index_open
            if index_open:
                dates = {
                    'date': [start_i.strftime('%Y/%m/%d\n%H:%M:%S')],
                    'open': [df_min.open[index_open[0]]],
                    'high': [df_min['high'].max()],
                    'low': [df_min['low'].min()],
                    'close': [df_min.close[index_close[0]]]
                }
                result_for_interval = pandas.DataFrame(dates)
                data_frame_result = data_frame_result.append(result_for_interval, ignore_index=True)
            start_i += delta
            end_i += delta
        if df_days.empty:
            break
        start_day = end_day
        end_day = start_day + pandas.Timedelta(days=1)
    return data_frame_result

def graph(data_frame, tick):
    """Function for calculating the construction of a candlestick chart.
    Returns an image with a graph.
    Where data_frame -- DataFrame with columns 'date', 'open', 'high', 'low', 'close',
          tick -- str, the nasdaq company code"""
    fig, axis = plt.subplots(figsize=(9, 7), dpi=110)
    tic = tick
    plt.title(tic, fontsize=18)
    plt.xlabel('Date and time', fontsize=14)
    plt.ylabel('Values', fontsize=14)
    plt.get_current_fig_manager().canvas.set_window_title("Your chart")
    plt.annotate('start: %s' %data_frame['date'][0],
                 xy=(0.01, 0.98), xycoords='axes fraction',
                 fontsize=11, horizontalalignment='left', verticalalignment='top')
    plt.annotate('end: %s' %data_frame['date'][len(data_frame)-1],
                 xy=(0.01, 0.90), xycoords='axes fraction',
                 fontsize=11, horizontalalignment='left', verticalalignment='top')
    formation = lambda x, pos: data_frame['date'][x] if x in data_frame.index else ''
    axis.xaxis.set_major_formatter(ticker.FuncFormatter(formation))
    axis.grid(linewidth=0.5,
              linestyle='dashed')
    candlestick2_ohlc(axis, data_frame['open'], data_frame['high'],
                      data_frame['low'], data_frame['close'], width=0.4)
    plt.show()
    return fig

def save(fig, name, path=None):
    """The function responsible for saving the chart in the specified directory,
    which includes checking for the presence of the specified directory.
    Where fig -- an image with a graph,
          name -- str, future name image,
          path -- str, path to the save directory."""

    form = 'png'
    if path is None:
        fig.savefig('{}.{}'.format(name, form), fmt='png')
    else:
        if os.path.isdir(path):
            os.chdir(path)
            fig.savefig('{}.{}'.format(name, form), fmt='png')
        else:
            os.mkdir(path)
            fig.savefing('{}.{}'.format(name, form), fmt='png')


PARSER = argparse.ArgumentParser()
PARSER.add_argument('-n', '--nasdag', action='store', help='Company code',
                    choices=['SBER', 'AAPL', 'GOOG', 'YNDX', 'AMZN'], type=str)
PARSER.add_argument('-i', '--interval', action='store', help='Time interval',
                    choices=[5, 30, 60, 120, 240, 720], type=int)
PARSER.add_argument('-p', '--pic_name', action='store', help='IMG name', type=str)
PARSER.add_argument('-f', '--folder', action='store', help='Save folder', type=str)


COMPANY_CODE = PARSER.parse_args().nasdag
TIME_INTERVAL = PARSER.parse_args().interval
IMG_NAME = PARSER.parse_args().pic_name
FOLDER = PARSER.parse_args().folder

DATEFRAME_OHLC = getting_data(COMPANY_CODE)
DATEFRAME_OHLC = my_ohlc(DATEFRAME_OHLC, TIME_INTERVAL)
PICTURE = graph(DATEFRAME_OHLC, COMPANY_CODE)
if IMG_NAME is not None:
    save(PICTURE, IMG_NAME, FOLDER)
