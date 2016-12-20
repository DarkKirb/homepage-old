#!/usr/bin/env python3
import traceback, sys, storage, cgi, cgitb, random, time, string, hashlib, re, datetime
from http import cookies
from libs.session import Session
session=Session()
cgitb.enable()
form=cgi.FieldStorage()
if not "seed" in form:
    raise ValueError("Missing field seed!")
if not "username" in form:
    raise ValueError("Missing field username!")
if not "email" in form:
    raise ValueError("Missing field email!")
if not "password" in form:
    raise ValueError("Missing field password!")
if not "password2" in form:
    raise ValueError("Missing field password2!")
if not "checkstr" in form:
    raise ValueError("Missing field checkstr!")
if not form["password"].value == form["password2"].value:
    raise ValueError("Passwords are not the same.")
seed=int(form["seed"].value)
random.seed(seed)
checkstr="".join(random.choice(string.ascii_lowercase) for _ in range(4))
if not checkstr == form["checkstr"].value:
    seed=0
    checkstring="Do you think I'm so stupid?"
    raise ValueError("You didn't enter the correct Captcha.")
username = cgi.escape(form["username"].value)
for f in range(storage.count("users")):
    if storage.get("users",f)["username"] == username:
        raise ValueError("This username already exists.")
email=cgi.escape(form["email"].value)
if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    raise ValueError("This is not a valid E-Mail address.")
salt=random.SystemRandom().randint(0,2**256)
if len(form["password"].value) < 8:
    raise ValueError("Password has to be at least 8 characters long.")
if not form["password"].value == form["password2"].value:
    raise ValueError("Passwords are not the same.")
password=hashlib.sha512((hashlib.sha256(form["password"].value.encode('utf-8')).hexdigest() + hashlib.sha256(repr(salt).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
storage.append("users", {"username":username, "email":email, "salt":salt, "password":password, "session":hashlib.sha1(repr(0).encode('utf-8')).hexdigest() })
session.login(username)
sys.stdout.buffer.write(("Content-type: text/html\r\n%s\r\n\r\n<html><head><script>window.location.replace(\"index.py\");</script></head></html>"%(session.get())).encode('utf8'))
print("Test?")
