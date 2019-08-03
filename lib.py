

import requests
import json

from . import api
from .auth import AuthAPI

def try_to_json(st):
    if isinstance(st,str):
        try:
            v = json.loads(st)
            return v
        except:
            pass
    return st

class GabAPI:
    auth = None

    def __init__(self,auth=None):
        if isinstance(auth,dict) or isinstance(auth,AuthAPI):
            self.set_auth(auth)

    # (local)=> set api auth dict/AuthAPI
    def set_auth(self,auth):
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

    def __opt__(self,data,options):
        if isinstance(options,dict):
            for n in options:
                data[n] = options[n]
        return data
                
    # (gab.api)=> new toot
    def toot(self,message,options=None):
        assert isinstance(message,str)==True
        data = self.__opt__({},options)
        data['status'] = message
        # request
        res = api.api(self.auth,'/api/v1/statuses',data)
        return res

    # (gab)=> search 
    def find_user(self,query,options=None):
        assert isinstance(query,str)==True
        data = self.__opt__({},options)
        data['q'] = query
        # request
        res = api.api(self.auth,'/api/v2/search',data)
        return res

    # (gab)=> get all notifications 
    def notifications(self):
        res = api.api(self.auth,'/api/v1/notifications',{})
        if res.status_code == 200:
            return res.json()
        return None

    # (gab)=> remove single notification
    def notification_remove(self,id):
        if not isinstance(id,str):
            return None
        res = api.api(self.auth,'/api/v1/notifications/dismiss',{"id":id})
        if res.status_code == 200:
            return res.json()
        return None

    # (gab)=> get all users followed by id user
    def user_following(self,id):
        if not isinstance(id,str):
            return None
        res = api.api(self.auth,'/api/v1/accounts/{}/following',{'id':id})
        if res.status_code == 200:
            return res.json()
        return None
        
    # (gab)=> endorse toot by id
    def retoot(self,id):
        if not isinstance(id,str):
            return None
        res = api.api(self.auth,'/api/v1/statuses/{}/reblog',{'id':id})
        if res.status_code == 200:
            return res.json()
        return None

    def correct(self):
        assert isinstance(self.auth,AuthAPI)
        self.auth.correct()