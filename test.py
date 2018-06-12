import sys
from db.data_layer import get_request, get_user_by_id, search_tvshow, get_tvshow_by_url, like_tvshow, unlike_tvshow

from pprint import pprint

TVMAZE_URL = 'http://api.tvmaze.com/search/{}?q={}'
# TEST CALL
url = TVMAZE_URL.format('shows', 'game')

# try:
#    user = get_user_by_id(1)
#    tvshow = get_tvshow_by_url('http://api.tvmaze.com/shows/333')

#    print(user.likes.all())
#    for like in user.likes.all():
#       print(like)
#       print('---------------------------')
#       sys.stdout.flush()
# except:
#    pass


# like_tvshow(1,1241)
unlike_tvshow(1,1241)
