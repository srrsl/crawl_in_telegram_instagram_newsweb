import os
from datetime import datetime 
from multiprocessing import Process, Pool
from configparser import RawConfigParser

from news_info import *
from instagram_crawler import *
from telegram import *
from save_telegram_post_class import *

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# run ==> uvicorn main:app --reload
app = FastAPI()


@app.get("/")
def date():
    date_str = datetime.now()
    date = date_str.strftime("%Y-%m-%d")
    time = date_str.strftime("%H:%M:%S")

    return time


@app.get("/detailed_instagram_page_info/{user}")  
def insta_crawler(user):
    return scrape_data(user)


@app.get("/instagram_page_summary_info/{user}")  
def insta_summary_crawler(user):
    return scrape_less_data(user)


@app.get("/instagram_comments/{shortcode}")  
def instagram_comments_crawler(shortcode:str):
    # "CDV9zsRJSW-"
    data = insta_shortcode_cmnt_downlaoder(shortcode)
    return data


@app.get("/teleg_info/{url:path}")  
def teleg_info(url:str):
    post = telegram_page_download_scroll()
    page_info = post.teleg_page_info(url)

    return page_info


@app.get("/teleg_web_post/{url:path}")  
def teleg_post(url:str):
    post = telegram_page_download_scroll()
    posts = post.main(url)

    return (posts)


@app.get("/teleg_web_post_api/{url:path}")  
def teleg_post_api(url:str):
    telegram_class = telegram_API()
    pool = Pool(5)
    data = pool.apply_async(telegram_class.teleg_ch_posts, (url,))

    return (data.get())


@app.get("/teleg_photo_api/{user:path}")  
def teleg_photo_api(user:str):
    telegram_class = telegram_API()
    heavy_process = Process( 
        target=  telegram_class.teleg_ch_photo,
        daemon=True,
        args=(user,)
    )
    heavy_process.start()
    return "Page photo downloaded successfully."

    
####################################### test case (it will show persian text in html)
import requests
from bs4 import BeautifulSoup as BS 
from six.moves.urllib import parse

@app.get("/css_test")
def css():  
    res = requests.get("https://www.farsnews.ir/")
    soup = BS(res.text, 'html.parser')
    data = soup.select('h3 > a')
    text = []
    for link in data:
        # print (link.get('href'))
        text.append(link.text)
    return (text)
 #######################################


@app.get("/{source_web}/{newsID}")   #("/<path:address>") it was  for inputting link from user 
def url_prroducer(source_web, newsID):
    news_obj = news(source_web)
    text = news_obj.news_data(newsID)
    return (text)


@app.get("/{source_web}")  
def news_headlines(source_web):
    try:
        news_obj = news(source_web)
    except:
        return "Wrong site"

    text = news_obj.news_headlines()
    return (text)