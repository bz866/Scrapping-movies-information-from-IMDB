"""
Date: July29 2017

Author: Binqian Zeng

Scrapping information of all movies from IMDB website with BeautifulSoup. Using Parallel computing to accelerate the whole process.


Information:
movies name; released date; rating; director and actors

Environment:
Python 3.6.0

Input: url string
Output: csv file with movies name, released date, rating, director and actors
csv format: sep = ',', encoding = 'utf-8'

Using:
terminal -> $python scrapping_cont_from_IMDB.py

"""

#import packages
from utlis import *
import numpy as np
import pandas as pd
import time
import multiprocessing

if __name__ == '__main__':
    #number of CPUs
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)

    #initiate a csv file 
    column_list = ['Name', 'Year', 'Rating', 'Director', 'Actors']
    df = pd.DataFrame(columns = column_list)
    df.to_csv('results.csv',sep=',', encoding='utf-8')

    #setup the page loop and year loop range
    years_url = [str(i) for i in range(1874,2118)]

    #initialize start time 
    start_time = time.time()
    #use all CPUs we have to scrap data
    pool.map(scrap_from_each_year, years_url)

    #print whole time 
    whole_time = time.time() - start_time
    print('The whole time for this scrapping is %s'%whole_time)













