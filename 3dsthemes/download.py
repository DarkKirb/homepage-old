#!/usr/bin/env python3
import cgi, sys, storage, cgitb, os, glob
cgitb.enable()
from libs import zip
def zipdir(path, ziph):
    olddir=os.getcwd()
    os.chdir(path)
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for f in files:
        print(f)
        ziph.append(f, open(f, "rb").read())
    os.chdir(olddir)
    
arguments = cgi.FieldStorage()
page=0
if "page" in arguments:
    page=int(arguments["page"].value)
else:
    raise ValueError("You have to supply a page number.")
article = storage.get("themes",int(page))
id=article["aid"]
if "deleted" in article and article["deleted"]:
    id=-1
ziph=zip.InMemoryZip()
zipdir("_/3dsthemes/%i/"%(id), ziph)
sys.stdout.buffer.write(("Content-Type: application/zip\r\nContent-Disposition: attachment; filename=\"%05d-%s.zip\"\r\n\r\n" % (id, article["title"])).encode("utf8")+ziph.read())
