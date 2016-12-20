#!/usr/bin/env python3
from htmlgen import *
import cgi
import sys
import storage
from libs import smdh
from libs.session import Session
session=Session()
html=htmlgen.HTMLgen(pagelayout.getLayoutXML().decode('utf-8'),"Home Page")
count=storage.count("themes")
arguments = cgi.FieldStorage()
page=0
if "page" in arguments:
    page=int(arguments["page"].value)
else:
    raise ValueError("You have to supply a page number.")
article = storage.get("themes",int(page))
them=smdh.SMDH("_/3dsthemes/%i/info.smdh"%article["aid"])
contents=them.read_smdh()
ahtml = """
<table>
<tr><th>Property</th><th>Value</th></tr>
<tr><td>Name</td><td>{name}</td></tr>
<tr><td>Description</td><td>{desc}</td></tr>
<tr><td>Author</td><td>{author}</td></tr>
<tr><td>Background music</td><td><audio controls><source src="_/3dsthemes/{id}/bgm.ogg" type="audio/ogg" /> </audio></td></tr>
</table>""".format(name=contents["EN"][0], desc=contents["EN"][1], author=contents["EN"][2], id=article["aid"])
html.appendHTML(ahtml)
if session.isLoggedIn():
    if session.getUserName() == "darklink":
        html.appendHTML("<a href=\"do_delete.py?page=%i\">Delete</a>"%article["aid"])
    if session.getUserName() == article["author"]:
        html.appendHTML("<input type=\"button\" onclick=\"unlist(%i);\" value=\"Unlist\" />"%article["aid"])
html.addArticle( **article)
sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite(True).encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())
