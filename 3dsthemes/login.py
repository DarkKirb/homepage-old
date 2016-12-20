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
html=htmlgen.HTMLgen(pagelayout.getLayoutXML().decode('utf-8'),"Home Page")
count=storage.count("themes")
arguments = cgi.FieldStorage()
page=0
if "page" in arguments:
    page=int(arguments["page"].value)
start=count-20-page*20
end=count-page*20
html.addArticle(title="Login", markdown="""

<form action="do_login.py" method="POST">
    <input placeholder="Username" name="username" /> <br />
    <p>Password: <input type="password" name="password" /> <br /> </p>
    <input type="submit" />
</form>
""", author="darklink", date=1475579447,aid=0)
sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite(True, False).encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())

