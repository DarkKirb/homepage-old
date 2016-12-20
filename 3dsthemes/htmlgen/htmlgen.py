import cgitb
import markdown2
import datetime
import storage
from libs.session import Session
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
    def addArticle(self, title, markdown, author="Importbot", date=0, aid=0, tags=None, likes=[]):
        name=title
        self.articles.append(markdown2.markdown(markdown, extras=["tables","spoiler"]))
        self.titles.append(name)
        self.authors.append(author)
        self.dates.append(date)
        self.ids.append(aid)
    def prependHTML(self, text):
        self.asideHTML=text+self.asideHTML
    def appendHTML(self, text):
        self.asideHTML=self.asideHTML+text
    def renderSite(self, comments=False, ordinary=True):
        nav=""
        x=len(self.titles)-1
        for title in self.titles[::-1]:
            nav=nav+("<a href=\"#%s\">%s</a><br/>" % (self.ids[x], title))
            x=x-1
        main=""
        x=len(self.articles)-1
        for article in self.articles[::-1]:
            if not comments:
                main=main+('<div id="%s" class="theme" data-nsfw="false"><a href="theme.py?page=%s"><div class="theme-onhover">%s</div><img class="theme-preview" src="_/3dsthemes/%s/Preview.png" style="" /></a></div>'%(self.ids[x], self.ids[x], article,self.ids[x]))
            else:
                if ordinary:
                    art=storage.get("themes", self.ids[x])
                    likes=0
                    if "likes" in art:
                        likes=len(art["likes"])
                    session=Session()
                    if not session.isLoggedIn():
                        main=main+("<h2>{title}</h2><p>Uploaded on <time datetime=\"{date1}\">{date2}</time> by {author}</p><article><img src=\"_/3dsthemes/{aid}/Preview.png\" alt=\"Theme image\" style=\"\" />{article}<br /><form action=\"download.py?page={aid}\"><input type=\"button\" onclick=\"dl({aid})\" value=\"⬇ Download Theme\" /><input type=\"button\" value=\"❤️{likes}\"/></form></article><aside>{aside}</aside>".format(
                            title=self.titles[x],date1=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%Y-%m-%d %H:%M:%S"),date2=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%c"),
                            author=self.authors[x],aid=self.ids[x],article=article,aside=self.asideHTML,likes=likes))
                    else:
                        if "likes" in art and session.getUserName() in art["likes"]:
                            main=main+("<h2>{title}</h2><p>Uploaded on <time datetime=\"{date1}\">{date2}</time> by {author}</p><article><img src=\"_/3dsthemes/{aid}/Preview.png\" alt=\"Theme image\" style=\"\" />{article}<br /><form action=\"download.py?page={aid}\"><input type=\"button\" onclick=\"dl({aid})\" value=\"⬇ Download Theme\" /><input type=\"button\" style=\"border-stlye:inset\" id=\"likes\" onclick=\"like({aid})\" value=\"❤️{likes}\"/></form></article><aside>{aside}</aside>".format(
                                title=self.titles[x],date1=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%Y-%m-%d %H:%M:%S"),date2=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%c"),
                                author=self.authors[x],aid=self.ids[x],article=article,aside=self.asideHTML,likes=likes))
                        else:
                            main=main+("<h2>{title}</h2><p>Uploaded on <time datetime=\"{date1}\">{date2}</time> by {author}</p><article><img src=\"_/3dsthemes/{aid}/Preview.png\" alt=\"Theme image\" style=\"\" />{article}<br /><form action=\"download.py?page={aid}\"><input type=\"button\" onclick=\"dl({aid})\" value=\"⬇ Download Theme\" /><input type=\"button\" style=\"border-stlye:inset\" id=\"likes\" onclick=\"like({aid})\" value=\"❤️{likes}\"/></form></article><aside>{aside}</aside>".format(
                                title=self.titles[x],date1=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%Y-%m-%d %H:%M:%S"),date2=datetime.datetime.fromtimestamp(self.dates[x]).strftime("%c"),
                                author=self.authors[x],aid=self.ids[x],article=article,aside=self.asideHTML,likes=likes))
                else:
                    main=main+("<h2 id=\"%i\">%s</h2><p>Written on <time datetime=\"%s\">%s</time> by %s</p><article>%s</article><aside>%s</aside>" %(self.ids[x],self.titles[x],datetime.datetime.fromtimestamp(self.dates[x]).strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.fromtimestamp(self.dates[x]).strftime("%c"),self.authors[x],article,self.asideHTML))
 #           if not comments:
#                main=main+("<a href=\"comments.py?aid=%i\">Comments (%i)</a>") % (self.ids[x], storage.count("comments-%i"%self.ids[x]))
            x=x-1
        styleargs = {"title":self.title,"nav":nav,"main":main,"footer":"Copyright 2016 Morten"}
        return '\n'.join([line for line in (self.layout%styleargs).split('\n') if line.strip() != ''])
