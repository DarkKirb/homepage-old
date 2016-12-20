import cgi, os, hashlib, random
from http import cookies
import storage

class Session:
    def __init__(self):
        try:
            self.recvcookies=cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
        except:
            self.recvcookies=cookies.SimpleCookie()
        self.sendcookies=cookies.SimpleCookie()
    def getCookie(self, name):
        if not name in self.recvcookies:
            raise ValueError(name + " is not a cookie")
        return self.recvcookies[name].value

    def setCookie(self, name, val):
        if isinstance(val, str):
            self.sendcookies[name]=val
            self.sendcookies[name]["secure"]="secure"
            self.sendcookies[name]["domain"]=".dark32.cf"
        else:
            self.sendcookies[name]=repr(val)
            self.sendcookies[name]["secure"]="secure"
            self.sendcookies[name]["domain"]=".dark32.cf"
            
    def getSessionID(self):
        return self.getCookie("session")
    
    def setSessionID(self, _id):
        self.setCookie("session", _id)

    def getUserName(self):
        _id=self.getSessionID()
        hashid=hashlib.sha256(_id.encode("utf-8")).hexdigest()
        ipaddr=hashlib.sha256(cgi.escape(os.environ["REMOTE_ADDR"]).encode("utf-8")).hexdigest()
        hid=hashlib.sha512((hashid+ipaddr).encode("utf-8")).hexdigest()
        for f in range(storage.count("users")):
            user=storage.get("users", f)
            if user["session"] == hid:
                return user["username"]
        raise ValueError("User is not logged in")

    def setUserName(self, name):
        _id=random.randint(1,2**256)
        hashid=hashlib.sha256(str(_id).encode("utf-8")).hexdigest()
        ipaddr=hashlib.sha256(cgi.escape(os.environ["REMOTE_ADDR"]).encode("utf-8")).hexdigest()
        hid=hashlib.sha512((hashid+ipaddr).encode("utf-8")).hexdigest()
        self.setSessionID(_id)
        for f in range(storage.count("users")):
            user=storage.get("users", f)
            if user["username"] == name:
                user["session"] = hid
            storage.put("users", f, user)
            return None
        raise ValueError("User does not exist.")
    
    def login(self, name):
        if not self.isLoggedIn():
            self.setUserName(name)
    
    def logout(self):
        if self.isLoggedIn():
            self.setSessionID(0) # 0 is an illegal session id.
    def isLoggedIn(self):
        try:
            self.getUserName()
        except:
            return False
        else:
            return True
    
    def get(self):
        return self.sendcookies.output()
