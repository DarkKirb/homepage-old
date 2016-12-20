from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from libs.session import Session
import cgi
def getLayoutXML():
    root = Element("html")
    root.set("lang","en")

    head = SubElement(root, "head")
    body = SubElement(root, "body")
    body.set("class", "themes")

    title = SubElement(head, "title")
    title.text = "n3dsthemes - the non-stupid way for custom 3ds themes - %(title)s"
    charset = SubElement(head, "meta")
    charset.set("charset","utf-8")
    viewport = SubElement(head, "meta")
    viewport.set("content", "width=device-width, initial-scale=1.0")
    link1 = SubElement(head, "link")
    link1.set("rel", "stylesheet")
    link1.set("type", "text/css")
    link1.set("href", "style.css")
    analytics=SubElement(head, "script")
    analytics.text="""
function like(page) {
    document.location.href="do_like.py?page="+page
}
function dl(page) {
    document.location.href="download.py?page="+page
}
function unlist(page) {
    if(confirm("Are you sure you want to unlist this theme? As of now, unlisted themes can't be relisted.")) {
        document.location.href="do_delete2.py?page="+page
    }
}
"""    
    topLink = SubElement(body, "a")
    topLink.set("id", "top")
    topLink.text="\n"
    modalblur = SubElement(body, "div")
    modalblur.set("class","modal-blur")
    navbar = SubElement(modalblur, "div")
    navbar.set("class", "navbar-fixed")
    nav = SubElement(navbar, "nav")
    nav.set("class", "light-red accent-4 nav-wrapper")
    page=0
    arguments=cgi.FieldStorage()
    if "page" in arguments:
        page=int(arguments["page"].value)
    goback = None
    if page != 0:
        goback = SubElement(nav, "a")
        goback.set("href", "?page=%i"%(page-1))
        goback.set("style", "color:white;font-size:2.5em")
        goback.text=u"←"
    h1 = SubElement(nav, "h2")
    h1.set("class", "brand-logo center")
    h1.text="n3DSThemes"
    goforward = SubElement(nav, "a")
    goforward.set("href", "?page=%i"%(page+1))
    goforward.set("style", "color:white;text-align:right;float:right;font-size:2.5em")
    goforward.text = u"→"
    marquee = SubElement(modalblur, "div")
    #marquee.set("id", "newsMarquee")
    marquee.set("class", "light-red accent-6")

    containerdivm = SubElement(marquee, "div")
    containerdivm.set("class", "center")
    session=Session()
    news1 = None
    news2 = None
    if not session.isLoggedIn():
        news1 = SubElement(containerdivm, "a")
        news1.set("href", "login.py")
        news1.set("style", "color:white;text-decoration:underline")
        news1.text="Login -"
        news2 = SubElement(containerdivm, "a")
        news2.set("href", "register.py")
        news2.set("style", "color:white;text-decoration:underline")
        news2.text="- Register"
    else:
        news1 = SubElement(containerdivm, "a")
        news1.set("style", "color:white")
        news1.text="Welcome back, %s -"%(session.getUserName())
        news2 = SubElement(containerdivm, "a")
        news2.set("href", "upload.py")
        news2.set("style", "color:white;text-decoration:underline")
        news2.text="- Upload"
    themes = SubElement(modalblur, "div")
    themes.set("id", "themes")
    themes.set("class", "row")
    themes.text="%(main)s"
    upbar = SubElement(body, "a")
    upbar.set("class", "upbar")
    upbar.set("href", "#top")
    upbar.set("style", "float:right")
    upbar.text=u"↑"

    return ElementTree.tostring(root)
