

import requests
import json

from . import api
from .auth import AuthAPI

# for gab paginations
def pagination_(o,a,b):
    if b=='rel="prev"' or b[:-1]=='rel="prev"':
        if len(a) > 3:
            o['prev']=a[1:-2]
    elif b=='rel="next"' or b[:-1]=='rel="next"':
        if len(a) > 3:
            o['next']=a[1:-2]
    return o
def pagination(l):
    out = {'prev':None,'next':None}
    if isinstance(l,str):
        l = l.split(' ')
        if len(l)==2:
            out = pagination_(out,l[0],l[1])
        if len(l)==4:
            out = pagination_(out,l[0],l[1])
            out = pagination_(out,l[2],l[3])
    return out

# main library
# i split api_requests_functions and dev_interaction_functions 
# for better reading and, if necessary, to use different params.
class GabAPI:
    auth = None
    
    def __init__(self,auth=None):
        if isinstance(auth,dict) or isinstance(auth,AuthAPI):
            self.set_auth(auth)
    
    def __opt__(self,data,options):
        if isinstance(options,dict):
            for n in options:
                data[n] = options[n]
        return data

    def __pagination__(self,header):
        if api.dict_has(header,'link'):
            header['link'] = pagination(header['link'])
        return header

    def __id_action__(self,api_,id,options={}):
        if not isinstance(id,str) or not isinstance(api_,str):
            return None
        opt =  self.__opt__({},options)
        opt['id'] = id
        res = api.api(self.auth,api_,opt)
        if res:
            if res.status_code == 200:
                res.headers = self.__pagination__(res.headers)
        return res

    def set_auth(self,auth):
        ''' Set class.auth, use dict or AuthAPI '''
        if isinstance(auth,dict):
            if auth.__class__.__has__("base_url"):
                if auth.__class__.__has__("token"):
                    self.auth = AuthAPI(auth["base_url"],auth["token"])
                    return
        if isinstance(auth,AuthAPI):
            auth.correct()
            self.auth = auth
            return
        raise Exception("Invalid authentication: ",auth)
                
    def toot_send(self,message,options=None):
        ''' Send toot/status to local account. 
            Usage: toot("hello world") '''
        assert isinstance(message,str)==True
        data = self.__opt__({},options)
        data['status'] = message
        # request
        res = api.api(self.auth,'/api/v1/statuses',data)
        if res.status_code == 200:
            return res
        return None
        
    def toot_get(self,id):
        ''' Get specific toot/status." 
            Usage: get_toot("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}',id)
        return res
        
    def toot_context(self,id):
        ''' Get specific toot/status context." 
            Usage: get_toot_context("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/context',id)
        return res

    def toot_reposts(self,id):
        ''' Get repost from specific toot/status." 
            Usage: get_retoots("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/reblogged_by',id)
        return res

    def toot_favorites(self,id):
        ''' Get favorites from specific toot/status." 
            Usage: get_toot_favorites("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/favourited_by',id)
        return res

    def toot_card(self,id):
        ''' Get card from specific toot/status." 
            Usage: get_toot_favorites("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/card',id)
        return res

    def toot_share(self,id):
        ''' Share toot/status by id." 
            Usage: toot_share("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/reblog',id)
        return res

    def toot_unshare(self,id):
        ''' Undo share of toot/status by id." 
            Usage: toot_unshare("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/unreblog',id)
        return res

    def toot_pin(self,id):
        ''' Pin toot/status by id." 
            Usage: toot_pin("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/pin',id)
        return res

    def toot_unpin(self,id):
        ''' Undo pin of toot/status by id." 
            Usage: toot_unpin("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/unpin',id)
        return res

    def toot_like(self,id):
        ''' Add to Favourite specific toot/status by id." 
            Usage: toot_like("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/favourite',id)
        return res

    def toot_unlike(self,id):
        ''' Undo Favourite of specific toot/status by id." 
            Usage: toot_unlike("12345") '''
        res = self.__id_action__('/api/v1/statuses/{}/unfavourite',id)
        return res

    def search(self,query,options=None):
        ''' General search. 
            Usage: search("cat groups") '''
        assert isinstance(query,str)==True
        data = self.__opt__({},options)
        data['q'] = query
        # request
        res = api.api(self.auth,'/api/v2/search',data)
        if res.status_code == 200:
            return res.json()
        return None

    def notifications(self):
        ''' Get unseen notifications. 
            Usage: notifications() '''
        res = api.api(self.auth,'/api/v1/notifications',{})
        if res.status_code == 200:
            return res.json()
        return None

    def notifications_clear(self):
        ''' Remove all notifications. 
            Usage: notifications_clear() '''
        res = api.api(self.auth,'/api/v1/notifications/clear',{})
        if res.status_code == 200:
            return res.json()
        return None

    def notification_remove(self,id):
        ''' Remove single notification. 
            Usage: notification_remove("12345") '''
        res = self.__id_action__('/api/v1/notifications/dismiss',id)
        return res

    def user(self,id):
        ''' Get user info." 
            Usage: user("12345") '''
        res = self.__id_action__('/api/v1/accounts/{}',id)
        return res

    def user_following(self,id,options={}):
        ''' Get users followed by specific user id."  
            Usage: user_following("12345") '''
        assert isinstance(options,dict)==True
        res = self.__id_action__('/api/v1/accounts/{}/following',id,options)
        return res

    def user_followers(self,id,options={}):
        ''' Get users that follow specific user id." 
            Usage: user_followers("12345") '''
        assert isinstance(options,dict)==True
        res = self.__id_action__('/api/v1/accounts/{}/followers',id,options)
        return res
        
    def user_toots(self,id,options={}):
        ''' Get users toots from specific user id." 
            Usage: user_toots("12345") '''
        assert isinstance(options,dict)==True
        res = self.__id_action__('/api/v1/accounts/{}/statuses',id,options)
        return res
        
    def user_follow(self,id):
        ''' Follow account by id." 
            Usage: user_follow("12345") '''
        res = self.__id_action__('/api/v1/accounts/{}/follow',id)
        return res

    def user_unfollow(self,id):
        ''' Unfollow account by id." 
            Usage: user_unfollow("12345") '''
        res = self.__id_action__('/api/v1/accounts/{}/unfollow',id)
        return res

    def user_search(self,query,options=None):
        ''' Find user account. 
            Usage: user_search("human") '''
        assert isinstance(query,str)==True
        data = self.__opt__({},options)
        data['q'] = query
        # request
        res = api.api(self.auth,'/api/v1/accounts/search',data)
        if res.status_code == 200:
            return res.json()
        return None

    def paginate(self,header,next,get=True,data={}):
        ''' Paginate the header links 
            Usage: paginate(res.headers,...) '''
        next = next==True
        get = get==True
        res = None
        url = None
        if api.dict_has(header,'link'):
            if next:
                if api.dict_has(header['link'],'next'):
                    url = header['link']['next']
            else:
                if api.dict_has(header['link'],'prev'):
                    url = header['link']['prev']
        if url and get==True:
            res = api.__get__(url,self.auth.get_header_auth())
        elif url:
            if not isinstance(data,dict):
                data = {}
            res = api.__post__(url,self.auth.get_header_auth(),data)
        if res:
            if res.status_code==200:
                res.headers = self.__pagination__(res.headers)
        return res
