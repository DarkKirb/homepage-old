#!/usr/bin/env python3
import cgi, cgitb, os, storage, shutil, time, sys
cgitb.enable()
from libs.session import Session
session=Session()
form = cgi.FieldStorage()
if not "page" in form:
    raise ValueError("Page is missing")

article = storage.get("themes",int(form["page"].value))
if not session.getUserName() == article["author"]:
    raise ValueError("Insufficient Previlegdes.")
article["deleted"] = True
storage.put("themes",article["aid"], article)
sys.stdout.buffer.write(("HTTP/1.1 205 Reset Content\r\n\r\n").encode('utf8'))
