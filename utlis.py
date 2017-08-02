#import packages
#from utlis import *
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time
from time import sleep
from random import randint
from IPython.core.display import clear_output
import re
from warnings import warn

# functions
def get_total_titles_numbers(response):
    html_soup = BeautifulSoup(response.text, 'html.parser')
    page_desc = html_soup.find_all("div", {"class": "desc"})
    num = 0
    for desc in page_desc:
        ls = re.findall(r'\d+', desc.text.replace(',','').replace(' ',''))
        num = max([int(s) for s in ls])
    return num


def get_name_list(container):
    result_list = []
    try:
        name = container.h3.a.text
        result_list.append(name)
    except:
        result_list.append(None)
    return result_list


def get_year_list(container):
    result_list = []
    try:
        year = container.h3.find('span', {"class": 'lister-item-year'}).text
        result_list.append(year)
    except:
        result_list.append(None)
    return result_list

def get_rating_list(container):
    result_list = []
    try:
        rating = float(container.strong.text)
        result_list.append(rating)
    except:
        result_list.append(None)
    return result_list

def get_director_actors_list(container):
    try:
        directors_ls = []
        actors_ls = []
        for link in container.find_all("a"):
            if 'li_dr' in link['href']:
                directors_ls.append(str(link.text))
            elif 'li_st' in link['href']:
                actors_ls.append(str(link.text))
    except:
        pass
    return directors_ls, actors_ls