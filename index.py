#!/usr/bin/env python3
from htmlgen import *
import sys
import storage
html=htmlgen.HTMLgen(pagelayout.getLayoutXML().decode('utf-8'),"Home Page")
count=storage.count("articles")
for i in range(count):
    try:
        article=storage.get("articles",i)
        if "homepage" in article["tags"]:
            html.addArticle(**article)
    except:
        html.addArticle(aid=i, **storage.get("articles",i))

sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite().encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())
