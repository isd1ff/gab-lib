import requests

from .auth import AuthAPI

def asst(a,b=True):
    assert a==b

def inst(a,b=True):
    return isinstance(a,b)

def _ai_(a,b,c=True):
    asst(inst(a,b),c)

def dict_has(d,k):
    _ai_(d,dict)
    _ai_(k,str)
    try:
        return d[k]!=None
    except:
        return False

def list_has(l,v):
    _ai_(l,list)
    for n in l:
        if n==v:
            return True
    return False

## ==
## api validations
## ==

# __assert_sample__ ====>
# (sample:dict)*
# (data:dict)*
def __assert_sample__(sample,data):
    _ai_(sample,dict)
    _ai_(data,dict)
    if not sample or not data:
        return False
    for n in data:
        if dict_has(sample,n):
            if not inst(sample[n],type(data[n])):
                raise Exception("Invalid [data] item:",n," should be: ",type(data[n]))
        else:
            print("Warning [data] item is not necessary:",n)
    return True

# request ===>
# (auth:AuthAPI)*
# (api:string)*
# (data:dict)*
# (get:bool)
def __request__(auth,api,data,get=False):
    _ai_(api,str)
    _ai_(data,dict)
    _ai_(auth,AuthAPI)
    req = None
    if get==True:
        p = ""
        for n in data:
            if len(p) > 0:
                p += "&"
            p += n+"="+data[n]
        req = requests.get(
            url= auth.base_url + api + '?' + p, headers=auth.get_header_auth())
    else:
        req = requests.post(
            url=auth.base_url + api, data=data, headers=auth.get_header_auth())
    return req


def __simple_get__(auth,api,data={}):
    r = __request__(auth,api,data,True)
    return r

def __simple_post__(auth,api,data={}):
    r = __request__(auth,api,data)
    return r

## ==
## api calls
## ==

def __toot__(auth,api,data):
    sample={"status":"",}
    __assert_sample__(sample,data)
    return __simple_post__(auth,api,data)

def __find__(auth,api,data):
    sample={"q":"","limit":0,"following":False,"resolve":False}
    __assert_sample__(sample,data)
    return __simple_get__(auth,api,data)

def __notif_dismiss__(auth,api,data={}):
    inst(data,dict)
    sample={"id":""}
    __assert_sample__(sample,data)
    return __simple_post__(auth,api,data)

def __user_following__(auth,api,data={}):
    inst(data,dict)
    sample={"id":""}
    __assert_sample__(sample,data)
    api = api.format(data['id'])
    return __simple_get__(auth,api,data)

def __retoot__(auth,api,data={}):
    inst(data,dict)
    sample={"id":""}
    __assert_sample__(sample,data)
    api = api.format(data['id'])
    return __simple_post__(auth,api,data)

__api__ = {
    '/api/v1/statuses':__toot__,
    '/api/v2/search':__find__,
    '/api/v1/accounts/{}/following':__user_following__,
    '/api/v1/notifications':__simple_get__,
    '/api/v1/notifications/clear':__simple_post__,
    '/api/v1/notifications/dismiss':__notif_dismiss__,
    '/api/v1/statuses/{}/reblog':__retoot__,
}

def api(auth,api,data):
    assert isinstance(auth,AuthAPI)==True
    assert isinstance(api,str)==True
    assert isinstance(data,dict)==True
    try:
        assert dict_has(__api__,api)==True
    except:
        print("API call not implemented => ",api)
        return None
    # validation
    auth.correct()
    try:
        response = __api__[api](auth,api,data)
    except Exception as e:
        print("API call error => ",e)
        response = None
    return response