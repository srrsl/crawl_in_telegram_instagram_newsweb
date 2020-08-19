from requests import get
from bs4 import BeautifulSoup as BS 
from json import loads
import json
import instaloader
import requests
from random import choice
from flask import jsonify

from instaloader import Instaloader
from instaloader.structures import *


def scrape_data(username):
    resp = get(f'https://instagram.com/{username}')
    if resp.status_code == 200:
        soup = BS(resp.text, 'html.parser')
        scripts = soup.find_all('script')

        data_script = scripts[4]

        content = data_script.contents[0]
        data_object = content[content.find('{"config"') : -1]
        data_json = loads(data_object)

    return data_json


def scrape_less_data(username):
    resp = get(f'https://instagram.com/{username}')
    if resp.status_code == 200:
        soup = BS(resp.text, 'html.parser')
        scripts = soup.find_all('script')

        data_script = scripts[4]

        content = data_script.contents[0]
        data_object = content[content.find('{"config"') : -1]
        data_json = loads(data_object)
        data_json = data_json['entry_data']['ProfilePage'][0]['graphql']['user']

        result = {
            'biography': data_json['biography'],
            'external_url': data_json['external_url'],
            'followers_count': data_json['edge_followed_by'],
            'following_count': data_json['edge_follow'],
            'full_name': data_json['full_name'],
            'is_private': data_json['is_private'],
            'username': data_json['username'],
            'total_posts': data_json['edge_owner_to_timeline_media']['count']
        }

    return result


def insta_shortcode_cmnt_downlaoder(shortcode):
    L = instaloader.Instaloader() 

    posts = Post.from_shortcode(L.context, shortcode)
    # print("posts comments counter :", posts.comments)

    comments_array = []
    for comment in posts.get_comments():
        comments = {}
        comments["text"] = (comment.text)
        datetime = comment.created_at_utc
        comments["created at"] = datetime.strftime("%Y-%m-%d , %H:%M:%S")
        comments["id"] = (comment.id)
        comments["owner"] = comment.owner.username

        comments_array.append(comments)
        # print(comments)
    
    return comments_array
