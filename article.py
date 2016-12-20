#!/usr/bin/env python3
import storage, sys, time
name = input("Name: ")
title = input("Title: ")
tags = input("Tags: ").split(' ')
article = '\n'.join(sys.stdin.readlines())
timestamp = int(time.time())
data={"name":title,"markdown":article,"author":name,"date":timestamp, "tags":tags, "aid":storage.count("articles")}
storage.append("articles",data)
