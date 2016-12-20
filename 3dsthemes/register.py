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
start=count-21-page*21
end=count-page*21
seed=random.SystemRandom().randint(0,2**24)
random.seed(seed)
checkstr="".join(random.choice(string.ascii_lowercase) for _ in range(4))
image = ImageCaptcha()
capt = image.generate(checkstr)
html.addArticle(title="Registration", markdown="""
This section allows you to register to this site. Registering gives you permission to upload own themes to the site. By registering you are accepting the following Terms of Service: (This agreement was last modified on October 4th, 2016.)

* The theme must be appropriate for children and adolescents.
* The theme must not infringe copyright.
    - You may upload themes created by others, unless the original author is against uploading the content.
    - You have to credit the original author (either with a name or a link to the original content)
* The theme must not violate German and international law.
* The theme must not contain misleading or offensive content.

Note that your access to the site can be revoked any time.

Note that, after you login, cookies will be stored on your device.

<form action="do_register.py" method="POST">
    <input type="hidden" name="seed" value="%i" />
    <input placeholder="Username" name="username" /> <br />
    <input placeholder="E-Mail" name="email" /> <br />
    <p>Password (min. 8 characters): <input type="password" name="password" /> <br /> </p>
    <p>Repeat Password: <input type="password" name="password2" /> <br /> </p>
    <img src="data:image/png;base64,%s" alt="Captcha image" /> <br />
    <input placeholder=\"Captcha. lower case only. case sensitive" name="checkstr" /> <br />
    <input type="submit" />
</form>
""" %(seed,base64.b64encode(capt.getvalue()).decode("UTF-8")), author="darklink", date=1475579447,aid=0)
sys.stdout.buffer.write("Content-type: text/html\r\n\r\n".encode('utf8'))
sys.stdout.buffer.write("<!DOCTYPE html>".encode('utf8'))
sys.stdout.buffer.write(html.renderSite(True, False).encode('utf8'))
sys.stdout.flush()
#print(html.renderSite())
