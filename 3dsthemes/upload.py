#!/usr/bin/env python3
from htmlgen import *
import cgi
import sys
import storage
import traceback
import random
import base64
from io import BytesIO
from captcha.image import ImageCaptcha
import time,string
from libs.session import Session
session=Session()
if not session.isLoggedIn():
    raise ValueError("Can't upload while not logged in.")

html=htmlgen.HTMLgen(pagelayout.getLayoutXML().decode('utf-8'),"Home Page")
count=storage.count("themes")
arguments = cgi.FieldStorage()
page=0
if "page" in arguments:
    page=int(arguments["page"].value)
start=count-20-page*20
end=count-page*20
html.addArticle(title="Upload a theme", markdown="""
Maximum file size: 20MB. File format: .zip
<form action="do_upload.py" method="POST" enctype="multipart/form-data">
    <input placeholder="Title" name="title" /> <br/>
    <textarea name="desc" placeholder="Description" cols="50" rows="10">Enter Message here. Markdown is enabled.</textarea> <br />
    <input name="file" type="file" accept="application/zip" /> <br />
    <input type="submit" />
</form>
""", author="darklink", date=1475579447,aid=0)
sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite(True, False).encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())

