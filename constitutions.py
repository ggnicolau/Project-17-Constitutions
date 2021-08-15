#%%
import tqdm
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

#%%
pip install selenium

#%%
# Call your driver
driver = webdriver.Firefox(executable_path="C:/Users/user/Documents/1. GitHub/zz.selenium_drivers/geckodriver.exe")
#driver = webdriver.Chrome(executable_path='C:/Users/user/Documents/1. GitHub/selenium_drivers/chromedriver.exe')

#%%%
# Set variables
url = 'https://www.constituteproject.org/constitutions?lang=en&status=in_force&status=is_draft'
response = requests.get(url)
response.text
driver.get(url)

elem = driver.find_element_by_tag_name('a')
print(elem)

#%%
# Make a Dataframe with link for each news
from tqdm import tqdm
from tqdm import trange
continue_link = driver.find_element_by_tag_name('a')
elem = driver.find_elements_by_xpath("//*[@href]")
elems = driver.find_elements_by_xpath("//a[@href]")
constitutions = []
for elem in tqdm(elems):    
    constitutions.append(elem.get_attribute("href"))
    #print(elem.get_attribute("href"))
    #print(capricho)
constitutions

#%%
# Save list
textfile = open("constitutions.txt", "w")
for element in constitutions:
    textfile.write(element + "\n")
textfile.close()


#%%
# Duplicates (not working)
constitutions = list(dict.fromkeys(constitutions))
print(constitutions)

#%%
import pandas as pd
corpus = pd.read_csv('C:/Users/user/Documents/1. GitHub/Projeto 17-Constitutions/constitutions.txt', header=None)
df = corpus.drop_duplicates()
# corpus.drop_duplicates(subset=None, keep='first', inplace=False)
df

#%% Filter only the constitutions
#df = df[df[0].str.contains('https://www.constituteproject.org/constitution/')]

#%% Bs4
url = 'https://www.constituteproject.org/constitution/Israel_2013?lang=en'
response = requests.get(url)
response.text
#%%
print(response.content) 

#%%
import requests 
from bs4 import BeautifulSoup 

url = 'https://www.constituteproject.org/constitution/Israel_2013?lang=en'
response = requests.get(url) 

soup = BeautifulSoup(response.content, 'html5lib') 
print(soup.prettify()) 


#%%
# Function to get name
list_name = []
title = soup.find("title")
#name = article["id"].split("-")[1]
#list_name.append(post_id)
title

#%%
# Function to get name
list_name = []
cons = soup.findAll("p")
#name = article["id"].split("-")[1]
#list_name.append(post_id)
cons

#%% Function to get full text
def article(x):
    c = []
    for wrapper in x:
        c.append(wrapper.text)
        #print (wrapper.text)
    return c
#%%
article(cons)

#%% Tables

import tqdm
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm


import pandas as pd
corpus = pd.read_csv('C:/Users/user/Documents/1. GitHub/Projeto 17-Constitutions/constitutions.txt', header=None)
df = corpus.drop_duplicates()
corpus.drop_duplicates(subset=None, keep='first', inplace=False)
#df.columns = ['links']
df = df.reset_index(drop=True)
df
#%%
#df["news_id"] = np.nan
#df["date"] = np.nan
#df["author"] = np.nan
df["name"] = np.nan
#df["subtitle"] = np.nan
df["text"] = np.nan
#%%
df
#%%

# Function to get full text
def article(x):
    c = []
    for wrapper in x:
        c.append(wrapper.text)
        #print (wrapper.text)
    return c


from tqdm import tqdm
from tqdm import trange



def full_table(x):
    j=0
    while tqdm(j<=x):
        try:
            url = df[0][j]
            response = requests.get(url, timeout=10)
            html = response.content
            soup = BeautifulSoup(html, 'html5lib')
            name =  soup.find("title").text
            df['name'].iloc[j] = name
            cons = soup.findAll("p")
            a = article(cons)
            df['text'].iloc[j] = a
            j+=1
        #print(df)
        except:
            j+=1
            pass
    print(df)
    return df

#%%
full_table(5)



#%%
url = df[0][176]
response = requests.get(url, timeout=10)
html = response.content
soup = BeautifulSoup(html, 'html5lib')
soup

#%%
name1 =  soup.find("title")
name1
#%%
cons = soup.findAll("p")
a = article(cons)
a
df['text'].iloc[1] = a
#%%
df['name'].iloc[1] = name1
#%%
df['name'][1]














#%%
# Scrap your table
full_table(5)


#%%
print(df[0])
# %%
soup.find("article").findAll('p')
# %%
