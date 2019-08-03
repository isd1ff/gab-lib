
# auth class for quick usage
class AuthAPI:
    base_url = None
    token = None

    def __init__(self):
        pass

    def __init__(self,base_url,token):
        self.set_base_url(base_url)
        self.set_token(token)

    def set_base_url(self,url):
        assert isinstance(url,str)==True
        self.base_url = url

    def set_token(self,token):
        assert isinstance(token,str)==True
        self.token = token

    def get_header_auth(self,bearer=True):
        assert isinstance(self.token,str)==True
        header = {}
        header['Authorization'] = ''
        if bearer:
            header['Authorization'] = 'Bearer '
        header['Authorization'] += self.token
        return header
    
    def correct(self):
        assert isinstance(self.base_url,str)==True 
        assert isinstance(self.token,str)==True 
