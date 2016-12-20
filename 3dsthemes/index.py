#!/usr/bin/env python3
from htmlgen import *
import cgi
import sys
import storage
html=htmlgen.HTMLgen(pagelayout.getLayoutXML().decode('utf-8'),"Home Page")
count=storage.count("themes")
arguments = cgi.FieldStorage()
page=0
if "page" in arguments:
    page=int(arguments["page"].value)
start=count-20-page*20
end=count-page*20
for i in range(start, end):
    theme=storage.get("themes", i)
    if "deleted" in theme:
        if not theme["deleted"]:
            del theme["deleted"]
        else:
            continue
    html.addArticle( **storage.get("themes",i))
sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite().encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())
