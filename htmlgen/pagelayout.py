from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree

def getLayoutXML():
    root = Element("html")
    root.set("lang","en")
    head = SubElement(root, "head")
    body = SubElement(root, "body")
    title = SubElement(head, "title")
    title.text = "%(title)s"
    charset = SubElement(head, "meta")
    charset.set("charset","utf-8")
    link1 = SubElement(head, "link")
    link1.set("rel", "stylesheet")
    link1.set("type", "text/css")
    link1.set("media", "screen and (max-width: 1023px)")
    link1.set("href", "mobilestyle.css")
    link2 = SubElement(head, "link")
    link2.set("rel", "stylesheet")
    link2.set("type", "text/css")
    link2.set("media", "screen and (min-width: 1024px)")
    link2.set("href", "mainstyle.css")
    meta = SubElement(head, "meta")
    meta.set("name", "viewport")
    meta.set("content", "width=device-width, initial-scale=1.0")
    topLink = SubElement(body, "a")
    topLink.set("id", "top")
    topLink.text="\n"
    title2 = SubElement(body, "h1")
    title2.text = "%(title)s"
    hr1 = SubElement(body, "hr")
    table = SubElement(body, "div")
    table.set("class", "table")
    tablerow = SubElement(table, "div")
    tablerow.set("class", "tablerow")
    navspoiler = SubElement(tablerow, "div")
    navspoiler.set("class", "spoilertitle")
    navspoiler.set("tabindex", "1")
    navspoiler.text = "Navigation"
    nav = SubElement(tablerow, "nav")
    nav.set("class","spoilerContent")
    nav.text="%(nav)s"
    main = SubElement(tablerow, "main")
    main.text="%(main)s"
    asidespoiler = SubElement(tablerow, "div")
    asidespoiler.set("class", "spoilertitle")
    asidespoiler.set("tabindex", "2")
    asidespoiler.text="Aside information"
    aside = SubElement(tablerow, "aside")
    aside.set("class", "spoilerContent")
    aside.text="%(aside)s"
    hr2 = SubElement(body, "hr")
    footer = SubElement(body, "footer")
    footer.text="%(footer)s"
    upbar = SubElement(body, "a")
    upbar.set("class", "upbar")
    upbar.set("href", "#top")
    upbar.set("style", "float:right")
    upbar.text=u"↑"

    return ElementTree.tostring(root)
