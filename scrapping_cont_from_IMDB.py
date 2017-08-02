"""
Date: July29 2017

Author: Binqian Zeng

Scrapping information of all movies from IMDB website. 

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
from warnings import warn
from utlis import *
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time
from time import sleep
from random import randint
from IPython.core.display import clear_output
import re
#from joblib import Parallel, delayed
#import multiprocessing
#from itertools import repeat
#from pathos.pools import ProcessPool as Pool
#from functools import partial

#set up result list
names = []
years = []
ratings=[]
directors_ls = []
actors_ls = []

#Preparing the monitoring of the loop
start_time_all = time.time()
requests = 0

#setup the page loop and year loop range
years_url = [str(i) for i in range(1874,2118)]

#For every year in the interval 1874 - 2017
for year_url in years_url:
    
    #find the maximum page number in this year
    response = get("http://www.imdb.com/search/title?release_date=" + year_url +
                   "&sort=alpha,asc&page=0&ref_=adv_nxt")
    
    num = get_total_titles_numbers(response)
    
    pages = int(num/50) + 1
    
    pages = [str(i) for i in range(pages)]
    
    start_time_page = time.time()
    
    #scrap infomation from evrey page
    for page in pages:
        #If error raised when request page, pass this page
        try:
            #Make a request
            url = ("http://www.imdb.com/search/title?release_date=" + year_url +
                       "&sort=alpha,asc&page="+page+'&ref_=adv_nxt')
            response = get(url)
            #Pause the loop
            sleep(randint(1,2))
            #Monitor the requests 
            requests += 1 
            elapsed_time = time.time() - start_time_page
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
            #clear_output(wait=True)

            #Throw a warning for non-200 status codes
            if response.status_code !=200:
                warn('Request:{}; Status code: {}'.format(requests, response.status_code))
                #Almost all warning are status=404, and all followings are 404. Break after first 404 page
                break

            #Parse the content of the request with BeautifulSoup
            page_html = BeautifulSoup(response.text, 'html.parser')

            #Get information of movies from a single page
            movie_containers = page_html.find_all("div", {"class": "lister-item mode-advanced"})

            for container in movie_containers:

                #The name 
                names.append(get_name_list(container))

                #The year
                years.append(get_year_list(container))

                #The IMDB rating
                ratings.append(get_rating_list(container))

                #The Director & stars
                rs_1, rs_2 = get_director_actors_list(container)
                directors_ls.append(rs_1)
                actors_ls.append(rs_2)
        except:
            pass

    #notice when one year scrapping is finished
    print('%s year finished.'%(year_url))

#print time of whole scrapping
end_time_all = time.time() - start_time_all
print(end_time_all)

#save results as dataframe
df = pd.DataFrame(list(zip(names, years, ratings, directors_ls, actors_ls)))
df.columns = ['Name', 'Year', 'Rating', 'Director', 'Actors']

#format the dataframe
for column in df.columns:
    df[column] = [i.strip('[').strip(']').strip("'").replace("', '",', ') for i in df[column].apply(str)]
df['Year'] = [i.strip('(').strip(')') for i in df['Year']]
    
#save results into csv file
df.to_csv('results.csv',sep=',', encoding='utf-8')









