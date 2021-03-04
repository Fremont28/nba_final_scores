#This script scrapes and retrieves final NBA scores from last afternoon or night’s action 

#import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re 
import numpy as np 
from datetime import datetime 
import requests 
import plotly.graph_objects as go

url="https://www.basketball-reference.com/boxscores/"
page=requests.get(url)
soup=BeautifulSoup(page.content)
soup_div=soup.find_all('div')

soup_div1=soup.find_all('td',class_=re.compile('right'))
soup_div2=soup.find_all('tr',class_=re.compile('winner'))
soup_div3=soup.find_all('tr',class_=re.compile('loser'))

nba_box1=[]
for f in soup_div1:
    print(f.get_text()) 
    nba_box1.append(f.get_text())

winner=[]
for f in soup_div2:
    print(f.get_text()) 
    winner.append(f.get_text())

loser=[]
for f in soup_div3:
    print(f.get_text()) 
    loser.append(f.get_text())

#extract team strings only (for winner/loser lists)
w=winner 
w=[]
for e in winner:
    parts=e.split('\n')
    w.append(parts)

w1=w
w1 = [item for sublist in w1 for item in sublist]
w1=[s.strip('\n') for s in w1]
w1=[s.strip('\t') for s in w1]
w1=[s.strip('\xa0') for s in w1]
w1=[s.strip('-') for s in w1]
w1=[s.strip('Final') for s in w1]
w1=[s.strip('OT') for s in w1]
w1=[x for x in w1 if x]

l=loser
l=[]
for e in loser:
    parts=e.split('\n')
    l.append(parts)

l1=l
l1 = [item for sublist in l1 for item in sublist]
l1=[s.strip('\n') for s in l1]
l1=[s.strip('\t') for s in l1]
l1=[s.strip('\xa0') for s in l1]
l1=[s.strip('-') for s in l1]
l1=[s.strip('Final') for s in l1]
l1=[s.strip('OT') for s in l1]
l1=[x for x in l1 if x]

#convert list to dataframes 
w2=np.array(w1)
w2_rows=w2.shape[0]/2 
w2_rows=int(w2_rows)
w2=w2.reshape(w2_rows,2)
w2=pd.DataFrame(w2)
w2.columns=['Winning Team','Winning Points']

l2=np.array(l1)
l2_rows=l2.shape[0]/2 
l2_rows=int(l2_rows)
l2=l2.reshape(l2_rows,2)
l2=pd.DataFrame(l2)
l2.columns=['Losing Team','Losing Points']

f_nba=pd.concat([w2,l2],axis=1)
f_nba=f_nba[["Winning Team","Losing Team","Winning Points","Losing Points"]]

max_points=f_nba.sort_values(by="Winning Points",ascending=True)
maxxie=max_points['Winning Team'][0]
maxxie 

f1= go.Figure(data=[go.Table(
    header=dict(values=list(f_nba.columns),
                fill_color='plum',
                align='left'),
    cells=dict(values=[f_nba['Winning Team'],f_nba['Losing Team'],f_nba['Winning Points'],f_nba['Losing Points']],
               fill_color='white',
               align='left')) ])

f1.update_layout(
    height=600,
    showlegend=False,
    title_text= maxxie  + " Got A Key Win Last Night",
)            
f1.show()




