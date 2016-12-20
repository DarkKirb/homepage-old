#!/usr/bin/env python3
import traceback, sys, storage, cgi, cgitb, random, time, string, hashlib, re, datetime, os
from http import cookies
from libs.session import Session
cgitb.enable()
session=Session()
form=cgi.FieldStorage()
if not "username" in form:
    raise ValueError("Missing field username!")
if not "password" in form:
    raise ValueError("Missing field password!")
username = form["username"].value

for f in range(storage.count("users")):
    user=storage.get("users",f)
    if user["username"] == username:
        salt=user["salt"]
        password=hashlib.sha512((hashlib.sha256(form["password"].value.encode('utf-8')).hexdigest() + hashlib.sha256(repr(salt).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
        if user["password"] != password:
            raise ValueError("Password incorrect")
        session.login(username)
        sys.stdout.write("Content-type: text/html\r\n%s\r\n\r\n<html><head><script>window.location.replace(\"index.py\");</script></head></html>\r\n"%(session.get()))
        sys.stdout.flush()
        

raise ValueError("User does not exist.")
