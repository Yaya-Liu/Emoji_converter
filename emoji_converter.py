# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:23:51 2020

@author: Yaya Liu
"""

import pandas as pd
from bs4 import BeautifulSoup as bsoup
import requests as rq
import re

base_usrl = "https://unicode.org/emoji/charts/full-emoji-list.html"


def convert_emoji_to_dict():
    print("Start extracting Emojis...")
    
    r = rq.get(base_usrl)
    soup = bsoup(r.text, features = "lxml")   
    trs = soup.find_all('tr')
    
    emoji_dict = {}
    
    for tr in trs:      
        tds = [td for td in tr.find_all('td')]
        if tds:
            code_list = []
            code = tds[1].text
            code_list = code.split()
            
            name = tds[-1].text   
            name = name.strip()   # remove the leading and ending spaces
            name = re.sub("[^a-zA-Z0-9]", " ", name)   # remove special letters
            
            #print(tds[0].text, code, name)
            
            if len(code_list) > 1:
                for i in code_list:
                    emoji_dict[i] = name                                   
            else:
                emoji_dict[code] = name
    #print(emoji_dict)
    
    df = pd.DataFrame(list(emoji_dict.items()), columns=['Code', 'Name'])   
    df.to_csv('Emoji.csv', index = False)
                      
    return emoji_dict


if __name__ == "__main__":
    convert_emoji_to_dict()