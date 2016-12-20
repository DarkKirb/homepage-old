#!/usr/bin/env python3
import cgi, cgitb, os, storage, shutil, time, sys
cgitb.enable()
from libs.session import Session
session=Session()
if not session.getUserName() == "darklink":
    raise ValueError("Insufficient priviledges.")

form = cgi.FieldStorage()
if not "page" in form:
    raise ValueError("Page is missing")

article = storage.get("themes",int(form["page"].value))
article["deleted"] = True
shutil.rmtree("_/3dsthemes/%i"%(article["aid"]))
storage.put("themes",article["aid"], article)
sys.stdout.buffer.write(("HTTP/1.1 205 Reset Content\r\n\r\n").encode('utf8'))
