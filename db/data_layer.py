import requests, json, sys
from pprint import pprint

from db.base import DbManager
from db.models import User, TVShow, Like

TVMAZE_SEARCH_URL = 'http://api.tvmaze.com/search/{}?q={}'
TVMAZE_URL = 'http://api.tvmaze.com/{}/{}'

# API FUNCTIONS
def get_request(url):
    response  = requests.get(url)
    return json.loads(response.text)

def search_tvshow(keyword):
    url = TVMAZE_SEARCH_URL.format('shows', keyword)
    data = get_request(url)
    
    tv_shows = []
    for tv_show in data:
        tvshow = TVShow()
        tvshow.parse_json(tv_show['show'])
        tv_shows.append(tvshow)
    return tv_shows

def like_tvshow(user_id, tvshow_id):
    user = get_user_by_id(user_id)

    tvshow_url = TVMAZE_URL.format('shows', tvshow_id)
    tvshow = get_tvshow_by_url(tvshow_url)

    DB = DbManager()
    try:
        exist = DB.open().query(Like).filter(Like.user_id == user_id, Like.tvshow_id == tvshow.id).one()
        return exist
    except:
        like = Like()
        like.user = user
        like.tvshow = tvshow
        DB.save(like)
        return like

def unlike_tvshow(user_id, tvshow_api_id):
    db = DbManager()
    tvshow = get_tvshow_by_api_id(tvshow_api_id)
    like = db.open().query(Like).filter(Like.user_id == user_id, Like.tvshow_id == tvshow.id).one()
    db.delete(like)
    return like

def get_tvshow_by_api_id(tvshow_api_id):
    db = DbManager()
    return db.open().query(TVShow).filter(TVShow.api_id == tvshow_api_id).one()

def get_tvshow_by_id(tvshow_id):
    db = DbManager()
    return db.open().query(TVShow).filter(TVShow.id == tvshow_id).one()

def get_tvshow_by_url(tvshow_url):
    DB = DbManager()
    try:
        tvshow = DB.open().query(TVShow).filter(TVShow.url == tvshow_url).one()
        DB.close()
        return tvshow
    except:
        DB = DbManager()
        data = get_request(tvshow_url)
        tvshow = TVShow()
        tvshow.parse_json(data)
        DB.save(tvshow)
        DB.close()
        return tvshow

def create_user(email, name, password):
    db = DbManager()
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_email(email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()
