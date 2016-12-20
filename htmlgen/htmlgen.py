import cgitb
import markdown2
import datetime
import storage
cgitb.enable()
class HTMLgen:
    def __init__(self, layout, title):
        self.layout=layout
        self.articles=[]
        self.titles=[]
        self.authors=[]
        self.dates=[]
        self.ids=[]
        self.title=title
        self.asideHTML=""
    def addArticle(self, name, markdown, author, date, aid, tags=None):
        self.articles.append(markdown2.markdown(markdown, extras=["tables","spoiler"]))
        self.titles.append(name)
        self.authors.append(author)
        self.dates.append(date)
        self.ids.append(aid)
    def prependHTML(self, text):
        self.asideHTML=text+self.asideHTML
    def appendHTML(self, text):
        self.asideHTML=self.asideHTML+text
    def renderSite(self, comments=False):
        nav=""
        x=len(self.titles)-1
        for title in self.titles[::-1]:
            nav=nav+("<a href=\"#%i\">%s</a><br/>" % (self.ids[x], title))
            x=x-1
        main=""
        x=len(self.articles)-1
        for article in self.articles[::-1]:
            main=main+("<h2 id=\"%i\">%s</h2><p>Written on <time datetime=\"%s\">%s</time> by %s</p><article>%s</article>" %(self.ids[x],self.titles[x],datetime.datetime.fromtimestamp(self.dates[x]).strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.fromtimestamp(self.dates[x]).strftime("%c"),self.authors[x],article))
            if not comments:
                main=main+("<a href=\"comments.py?aid=%i\">Comments (%i)</a>") % (self.ids[x], storage.count("comments-%i"%self.ids[x]))
            x=x-1
        if not comments:
            styleargs = {"title":self.title,"nav":nav,"main":main,"aside":self.asideHTML,"footer":"Copyright 2016 Morten"}
        else:
            styleargs = {"title":self.title,"nav":nav,"main":self.asideHTML+main,"aside":"","footer":"Copyright 2016 Morten"}
        return '\n'.join([line for line in (self.layout%styleargs).split('\n') if line.strip() != ''])
