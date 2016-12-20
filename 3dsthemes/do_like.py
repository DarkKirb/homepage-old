#!/usr/bin/env python3
import cgi, cgitb, os, storage, shutil, time, sys
cgitb.enable()
from libs.session import Session
session=Session()
if not session.isLoggedIn():
    raise ValueError("Must be logged in to like a theme")
form = cgi.FieldStorage()
if not "page" in form:
    raise ValueError("Page is missing")

article = storage.get("themes",int(form["page"].value))
if not "likes" in article:
    article["likes"]=[]
username=session.getUserName()
if not username in article["likes"]:
    article["likes"].append(username)
else:
    article["likes"]=list(filter((username).__ne__, article["likes"]))


storage.put("themes",int(form["page"].value), article)
sys.stdout.buffer.write(("HTTP/1.1 205 Reset Content\r\n\r\n").encode('utf8'))
print("Test?")

