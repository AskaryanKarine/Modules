"""Программа обрабатывает данные для построения свечных графиков
    с масштабами 5 минут, 30 минут, 240 минут"""
#В процессе работы над модульным проектом, работа происходила следующим образом:
#Аскарян К. - работа с библиотекой pandas, запись в файл, проверка кода через pylint
#Колесов И. - работа с библиотекой argparse, проверка кода через pylint
#Иванов И. - поиск информации, моральная поддержка.

import argparse
import pandas

def ohlc_for_minutes(data_frame_days, left_date, right_date):
    """Функция считает OHLC для заданного единичного интервала"""
    b_date = (data_frame_days['DateTime'] >= left_date) & (data_frame_days['DateTime'] < right_date)
    interval_minutes = data_frame_days[b_date]
    interval_ohlc = interval_minutes.groupby(['Company'])['Price'].ohlc().sort_values(by='open')
    return interval_ohlc

def ohlc_for_intervals(data_frame, interval):
    """Функция возвращает таблицу обработанных данных для
        построение свечного графика для заданного интервала"""
    delta = pandas.Timedelta(minutes=interval)
    date1 = pandas.to_datetime('2019-01-30 07:00:00.00000')
    date2 = pandas.to_datetime('2019-01-31 03:00:00.00000')
    date3 = date1
    date5 = date3
    data_frame_res = None
    while True:
        bool_dates = (data_frame['DateTime'] >= date1) & (data_frame['DateTime'] < date2)
        interval_day = data_frame[bool_dates]
        interval_min = ohlc_for_minutes(interval_day, date3, date3+delta)
        while not interval_min.empty:
            interval_min = ohlc_for_minutes(interval_day, date3, date3+delta)
            date5 = date5.strftime('%y-%d-%mT%XZ')
            date3 += delta
            if not interval_min.empty:
                dates = pandas.Series([date5]*(interval_min.size//4), index=interval_min.index)
                data_frame_dates = pandas.DataFrame(dates)
                data_frame_dates = data_frame_dates.join(interval_min)
                data_frame_res = pandas.concat([data_frame_res, data_frame_dates])
            date5 = date3
        date1 += pandas.Timedelta(days=1)
        date2 += pandas.Timedelta(days=1)
        date3 = date1
        if interval_day.empty:
            break
    return data_frame_res


PARSER = argparse.ArgumentParser()
PARSER.add_argument('--file', action='store', help='Open file')
PARSER.add_argument('--full_info', action='store_const', const='1', help='All about function')
if PARSER.parse_args().full_info == '1':
    print('func1 : ohlc_for_minutes-counts OHLC for a given unit interval')
    print('func2 : ohlc_for_intervals-return table processed data')
WAY = PARSER.parse_args().file

if  WAY is not None:
    DATA_FRAME_READ = pandas.read_csv(WAY, names=['Company', 'Price', 'Amount', 'DateTime'])
    DATA_FRAME_READ['DateTime'] = pandas.to_datetime(DATA_FRAME_READ['DateTime'])
    OHLC_240MIN = ohlc_for_intervals(DATA_FRAME_READ, 240)
    OHLC_5MIN = ohlc_for_intervals(DATA_FRAME_READ, 5)
    OHLC_30MIN = ohlc_for_intervals(DATA_FRAME_READ, 30)
    pandas.set_option('display.float_format', '{:g}'.format)
    OHLC_5MIN.to_csv('ohlc_5min.csv', header=False)
    OHLC_30MIN.to_csv('ohlc_30min.csv', header=False)
    OHLC_240MIN.to_csv('ohlc_240min.csv', header=False)
