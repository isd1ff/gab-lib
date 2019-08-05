import requests

from .auth import AuthAPI


def asst(a,b=True):
    assert a==b

def inst(a,b=True):
    return isinstance(a,b)

def _ai_(a,b,c=True):
    asst(inst(a,b),c)

def dict_has(d,k):
    if d:
        try:
            return d[k]!=None
        except:
            return False
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
    return True

# request ===>
# (auth:AuthAPI)*
# (api:string)*
# (data:dict)*
# (get:bool)
def __get__(url,header):
    res = requests.get(url=url, headers=header, allow_redirects=False)
    return res
def __post__(url,header,data):
    res = requests.post(url=url, data=data, headers=header, allow_redirects=False)
    return res
def __request__(auth,api,data,get=False):
    _ai_(api,str)
    _ai_(data,dict)
    _ai_(auth,AuthAPI)
    res = None
    if get==True:
        p = ""
        for n in data:
            if len(p) > 0:
                p += "&"
            p += n+"="+str(data[n])
        res = __get__(auth.base_url + api + '?' + p,auth.get_header_auth())
    else:
        res = __post__(auth.base_url + api,auth.get_header_auth(),data)
    return res

## ==
## API calls + validations
## ==
def __simple_get__(auth,api,data={}):
    r = __request__(auth,api,data,True)
    return r

def __simple_post__(auth,api,data={}):
    r = __request__(auth,api,data)
    return r

def __get_by_id__(auth,api,data):
    inst(data,dict)
    sample={"id":""}
    __assert_sample__(sample,data)
    api = api.format(data['id'])
    return __simple_get__(auth,api,data)

def __post_by_id__(auth,api,data):
    inst(data,dict)
    sample={"id":""}
    __assert_sample__(sample,data)
    api = api.format(data['id'])
    return __simple_post__(auth,api,data)

def __toot__(auth,api,data):
    sample={"status":"",}
    __assert_sample__(sample,data)
    return __simple_post__(auth,api,data)

def __get_retoot__(auth,api,data):
    inst(data,dict)
    sample={"id":"","limit":0}
    __assert_sample__(sample,data)
    api = api.format(data['id'])
    return __simple_get__(auth,api,data)

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


# still mapping samples,
# for now we will repeat some calls.
__api__ = {
    '/api/v1/statuses':__toot__,
    '/api/v1/statuses/{}':__get_by_id__,
    '/api/v1/statuses/{}/context':__get_by_id__,
    '/api/v1/statuses/{}/card':__get_by_id__,
    '/api/v1/statuses/{}/reblog':__post_by_id__, 
    '/api/v1/statuses/{}/reblogged_by':__get_retoot__,
    '/api/v1/statuses/{}/favourited_by':__get_retoot__,
    '/api/v1/statuses/{}/unreblog':__post_by_id__,
    '/api/v1/statuses/{}/favourite':__post_by_id__,
    '/api/v1/statuses/{}/unfavourite':__post_by_id__,
    '/api/v1/statuses/{}/pin':__post_by_id__,
    '/api/v1/statuses/{}/unpin':__post_by_id__,
    '/api/v2/search':__find__,
    '/api/v1/accounts/search':__find__,
    '/api/v1/accounts/{}':__get_by_id__,
    '/api/v1/accounts/{}/statuses':__get_by_id__,
    '/api/v1/accounts/{}/following':__get_by_id__,
    '/api/v1/accounts/{}/followers':__get_by_id__,
    '/api/v1/accounts/{}/follow':__post_by_id__,
    '/api/v1/accounts/{}/unfollow':__post_by_id__,
    '/api/v1/notifications':__simple_get__,
    '/api/v1/notifications/clear':__simple_post__,
    '/api/v1/notifications/dismiss':__notif_dismiss__
}

def api(auth,api,data):
    ''' Make request to api, using auth.'''
    _ai_(auth,AuthAPI)
    _ai_(api,str)
    _ai_(data,dict)
    try:
        asst(dict_has(__api__,api))
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