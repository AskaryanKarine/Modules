The work on the project was as follows:    
Аскарян К. (GitHub - github.com/AskaryanKarine) - тимлид, обработка данных, построение лайф-свечных графиков    
Гормакова М. (GitHub - github.com/Tenedra) - поиск API, получение данных    
Иванов И. (GitHub - github.com/tbR12) - сохранение графиков    
Колесов И. (GitHub - github.com/enotik1poloskyn) - работа с аргументами командной строки     

Libraries are required to work correctly with this program:     
requests v.2.22.0,      
pandas v.0.24.2,      
matplotlib v.3.1.0,      
mpl-finance v.0.10.0    

### Examples of running CLI-commands:  
```
List CLI-commands:
-h, --help - show all CLI-comands and short description.    
-n, --nasdaq - company code from the set SBER, AAPL, GOOG, YAND, AMZN.     
-i, --interval - interval (in minutes) building a candlestick chart.     
-p, --pic_name - chart name, with which candlestick chart was save. If this parameter not specifed , don`t save image.    
-f, --folder - name of directory ,where chart was save. If directory not exsist ,it needs to be created. If this parameter is not specified, you must save it to the application launch directory (if -p is present)
```
```
Examples of running: python main.py -n=AAPL -i=5
In this example, the user will get an image of a life candle chart based on data from Apple Inc. at intervals of 5 minutes, but the graph image will not be saved.
```

### List functions:
```
getting_data
    Function for receiving data from the Finam (SBER) and Tiingo (others).
    The function accepts the nasdaq company code.
    Returns a minute-by-minute DataFrame in the OHLC format
```
```
my_ohlc
    Function for calculating OHLC for a given period of time.
    Returns a DataFrame in OHLC format
    where data_frame -- a minute-by-minute DataFrame in the OHLC format,
          interval -- int, time interval in minutes, by default 5 minutes.
```
```
graph:
    Function for calculating the construction of a candlestick chart.
    Returns an image with a graph.
    Where data_frame -- DataFrame with columns 'date', 'open', 'high', 'low', 'close',
          tick -- str, the nasdaq company code.
```
```
save
    The function responsible for saving the chart in the specified directory,
    which includes checking for the presence of the specified directory.
    Where fig -- an image with a graph,
          name -- str, future name image,
          path -- str, path to the save directory.
```