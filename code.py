import requests
import csv
from bs4 import BeautifulSoup
import os

def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def write_title(data):   
    with open('zagolovki.csv', 'a+') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow((data['count'],data['title']
        ))  
def write_url(data): 
    with open('url.csv', 'a+') as f:
        writer = csv.writer(f)
        writer.writerow([data['url']
        ])  
def write_text(data): 
    with open('text.csv', 'a+') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow([data['text']
        ])
def write_foto(data): 
    with open('foto.csv', 'a+') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow([data['foto']
        ])  

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div',class_="Tag--articles")
    products = product_list.find_all('div',class_="Tag--article")
    count=0
    os.remove('zagolovki.csv')
    os.remove('url.csv')
    os.remove('text.csv')
    os.remove('foto.csv')
    for product in products:
        
        count+=1   
        try:
            title = product.find('div',class_="ArticleItem--data ArticleItem--data--withImage").find('a',class_="ArticleItem--name").text.replace('"','').replace('\n','')
        except:
            title = ''      
        try:
            href = product.find('div', class_="ArticleItem--data ArticleItem--data--withImage").find('a',class_="ArticleItem--name").get('href').replace(',','')
        except:
            href = ''
        try:
            foto=product.find('div', class_="ArticleItem--data ArticleItem--data--withImage").find('a',class_='ArticleItem--image').find('img').get('src')    
        except:
            foto=''
        title={'count':count,'title':title}
        write_title(title)
        text(get_text(href))
        href={'url':href}
        write_url(href)       
        foto={'foto':foto}
        write_foto(foto)
        if count==10:
            break
        
def get_text(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def text(html):
    soup = BeautifulSoup(html, 'lxml')
    paragraphs=soup.find('div',class_="Article--block").find_all('p')
    new=[]
    count=0
    for paragraph in paragraphs:
        count+=1
        try:
            text=paragraph.text
        except:
            text=''  
        new.append(text) 
        if count==2:
            break
    text={'text':new}
    write_text(text)
def main():
    from datetime import datetime
    time=str(datetime.now())[:10]
    url = f'https://kaktus.media/?date={time}&lable=8&order=time'
    get_page_data(get_html(url))
main()