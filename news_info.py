from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json 
import re
from configparser import RawConfigParser

class news:  
    def __init__(self, source_web):   
        config = RawConfigParser()

        config.read('config_'+source_web+'_ir.conf')
        self.setting = dict(config.items('news_config'))

    def news_data(self, newsID):    
        text = {}

        url = self.setting['url_name'] + newsID
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        head = soup.find('title')

        date_str = datetime.now()
        date_time = date_str.strftime("%Y-%m-%d , %H:%M:%S")
        text["query_date_time"] = date_time 
        text["url"] = url 
        text["title"] = [d.text for d in soup.find_all(self.setting['title_tag'], {self.setting['title_attr_key']:self.setting['title_attr_value']})]  
        text["summary"] = [d.text.strip() for d in soup.find_all(self.setting['summary_tag'], {self.setting['summary_attr_key']:self.setting['summary_attr_value']})]  
        text["body"] = [re.sub(r'\n','', d.text) for d in soup.find_all(self.setting['body_tag'], {self.setting['body_attr_key']:self.setting['body_attr_value']})]
        text["date"] = [re.sub(r'\n','', d.text) for d in soup.find_all(self.setting['date_tag'], {self.setting['date_attr_key']:self.setting['date_attr_value']})]

        key_words = []
        for d in soup.find_all(self.setting['keywords_tag'], {self.setting['keywords_attr_key']:self.setting['keywords_attr_value']}):
            if d.text not in key_words:
                txt = ' '.join(d.text.split())
                key_words.append(re.sub(r'\r\n','', txt))
        text["keywords"] = key_words
        
        with open(self.setting['name']+'_news.json', 'w') as json_file:
            json.dump(text, json_file)

        return text


    def news_headlines(self):    
        text = {}

        source = requests.get(self.setting['headlines']).text    
        soup = BeautifulSoup(source, 'lxml')

        date_str = datetime.now()
        date_time = date_str.strftime("%Y-%m-%d , %H:%M:%S")
        text["query_date_time"] = date_time 
        text["url"] = self.setting['headlines']  
        text["headlines"] = [re.sub(r'\n|\r|\s\s+','', d.text) for d in soup.find_all(self.setting['headline_tag'], {self.setting['headline_attr_key']:self.setting['headline_attr_value']})]
            
        with open(self.setting['name']+'_news_headlines.json', 'w') as json_file:
            json.dump(text, json_file)

        return text

# news_obj = news('isna')
# print(news_obj.news_data('99052820712'))
# print(news_obj.news_headlines())


# news_obj = news('isna')
# print(news_obj.news_data('99052820712'))
# print(news_obj.news_headlines())


# news_obj = news('isna')
# print(news_obj.news_data('99052820712'))
# print(news_obj.news_headlines())