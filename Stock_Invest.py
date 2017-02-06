# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 10:59:58 2016

@author: Pratibha
"""
########### Stock Investing ##################
import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import re
style.use("dark_background")

path="C:/Users/Pratibha/Documents/Python Scripts/Python_MachineLearning/intraQuarter"

def KeyStat(gather="Total Debt/Equity (mrq)"):
    Stats_path= path+'/_KeyStats'
    #print Stats_path
    Stock_list=[x[0] for x in os.walk(Stats_path)]
    #print Stock_list
    df=pd.DataFrame(columns=['Date',
                             'Unix',
                             'Ticker',
                             'DE Ratio',
                             'Price',
                             'stock_p_change',
                             'SP500',
                             'sp500_p_change',
                             'Difference',
                             'Status'])
    
    #new data frame
    sp500_df=pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    ticker_list=[]
    for each_dir in Stock_list[1:11]:
        #print each_dir
        each_file=os.listdir(each_dir)
        #print each_file
        #time.sleep(10)
        ticker=each_dir.split("\\")[1]
        ticker_list.append(ticker)
        
        starting_stock_value=False
        starting_sp500_value=False
        
        if each_file > 0:
            for file in each_file:
                date_stamp=datetime.strptime(file,'%Y%m%d%H%M%S.html')
                #print (date_stamp)
                unix_time=time.mktime(date_stamp.timetuple())
                # unix_time
              
                full_file_path=each_dir+'/'+ file
                #print(full_file_path)
                source=open(full_file_path,'r').read()
                try:
                    try:
                        value=float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    #print ticker+":",value
                    except Exception as e:
                        value=float(source.split(gather+':</td\n><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        print(str(e),ticker,file)
                        time.sleep(10)
                        
                        
                    try:
                        sp500_date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        #print "1:",sp500_df.index
                        #print "2:",sp500_date
                        
                        row=sp500_df[(sp500_df.index == sp500_date)]
                        #print row
                        sp500_value=float(row["Adjusted Close"])
                    except:
                        sp500_date=datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row=sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value=float(row["Adjusted Close"])
                    try:  
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        #<span id="yfs_l10_abc">43.05</span>
                    #print 'SP:',stock_price
                    except Exception as e:
                        try:
                            stock_price=(source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price=re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price=float(stock_price.group(1))
                            
                            #print(stock_price)
                            #time.sleep(10)
                            #print(str(e),ticker,file)
                        except Exception  as e:
                            stock_price=(source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            stock_price=re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price=float(stock_price.group(1))
                            
                            #print('Latest',stock_price)
                            #print('stock price',str(e),ticker,file)
                            #time.sleep(10)
                    if not starting_stock_value:
                        starting_stock_value=stock_price
                    if not starting_sp500_value:
                        starting_sp500_value=sp500_value                           
                    
                    stock_p_change =((stock_price-starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change=((sp500_value-starting_sp500_value) / starting_sp500_value) * 100
                    
                    
                    difference=stock_p_change - sp500_p_change
                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"
                        
                    df=df.append({'Date':date_stamp,
                                  'Unix':unix_time,
                                  'Ticker':ticker,
                                  'DE Ratio':value,
                                  'Price':stock_price,
                                  'stock_p_change':stock_p_change,
                                  'SP500':sp500_value,
                                  'sp500_p_change':sp500_p_change,
                                  'Difference':difference,
                                  'Status':status},ignore_index=True)
                except Exception as e:
                    pass
                    #print(str(e))
    for each_ticker in ticker_list:
        try:
            plot_df=df[(df['Ticker']== each_ticker)]
            plot_df = plot_df.set_index(['Date'])
            
            if plot_df['Status'][-1] == "underperform":
                color='m'
            else:
                color='g'
            
            plot_df['Difference'].plot(label=each_ticker,color=color)
            
            plt.legend()
        except:
            pass
        
    plt.show()
    save=gather.replace(' ','').replace('/','').replace('(','').replace(')','') +('.csv')
    print(save)
    df.to_csv(save)
                
                
                
            
            #time.sleep(10)
                
KeyStat()
    
