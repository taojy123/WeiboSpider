#coding=utf8

import cookielib
import urllib2, urllib
import time
import re
import traceback
import time
import json
import pickle
from BeautifulSoup import BeautifulSoup


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.ProxyHandler({'http':"10.239.120.37:911"}))
opener.addheaders = [
                    ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
                    ("Accept-Encoding","gzip,deflate,sdch"),
                    ("Accept-Language","zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4"),
                    ("Cache-Control","max-age=0"),
                    ("Cookie","TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; SUB=_2AkMiV0sAdcNhrAJQm_4czm_rb45Pjlmr45_wMk3sJxEzHhl_7T9l_xxrtXG-79OLSL7AcpgsgYXazcCRyk8-; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WWdv9aAphFaXjOIqMsvPocH5JpVFGxydcD4eKz0; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; _s_tentry=-; Apache=1236543264240.0264.1426834633528; SINAGLOBAL=1236543264240.0264.1426834633528; ULV=1426834633665:1:1:1:1236543264240.0264.1426834633528:"),
                    ("Host","weibo.com"),
                    ("Proxy-Connection","keep-alive"),
                    ("RA-Sid","1B736F8A-20150109-013640-a1edc4-5e3f41"),
                    ("RA-Ver","2.8.9"),
                    ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1964.4 Safari/537.36"),
                     ]
 
def get_page(url, data=None):
    print url
    resp = None
    n = 0
    while n < 3:
        n = n + 1
        try:
            resp = opener.open(url, data, timeout=8)
            page = resp.read()
            # page = page.decode("gbk", "replace").encode("gbk", "replace")
            return page
        except:
            traceback.print_exc()
            time.sleep(2)
            print "Try after 2 seconds ..."
            continue
    raise Exception("Get page failed")


def recovery(s):
    s = s.replace("$$$", "\\u")
    s = 'u"""' + s + '"""'
    s = eval(s)
    return s 



open("d.txt", "a")
s = open("d.txt").read()

if s:
    total = pickle.loads(s)
    print "loaded ok"
else:
    n = input("Max page:") + 1

    total = []
    mids = []

    for page in range(1, n):

        url="http://www.weibo.com/p/1005055413811165?page=%d" % page

        p = get_page(url)
        while "WB_feed WB_feed_profile" not in p:
            p = get_page(url)
            print "..."
            time.sleep(3)

        # open("a.html", "w").write(p)

        s = re.findall(r'<div class=\\"WB_feed WB_feed_profile\\">.*?"}', p)[0]

        # print s

        s = s[:-2]
        s = s.replace("\\r","").replace("\\n","").replace("\\t","")
        s = s.replace("\\","")

        # print s

        soup = BeautifulSoup(s)

        rs = soup.findAll("div", "WB_cardwrap WB_feed_type S_bg2")
        for r in rs:
            mid = r.get("mid")
            print mid
            mids.append(mid)
            content = r.find("div", "WB_text W_f14").getText()
            info = r.find("div", "WB_from S_txt2").getText()
            content = content.encode("gbk")
            info = info.encode("gbk")
            total.append(dict(content=content, info=info))
            print content, info

        i = 0
        flag = True
        while flag:

            url = "http://weibo.com/p/aj/v6/mblog/mbloglist?page=%d&pre_page=%d&pagebar=%d&id=1005055413811165" % (page, page, i)
            p = get_page(url)

            s = re.findall(r'<div .*?"}', p)[0]

            s = s[:-2]
            s = s.replace("\\r","").replace("\\n","").replace("\\t","").replace("\\u","$$$")
            s = s.replace("\\","")

            soup = BeautifulSoup(s)

            rs = soup.findAll("div", "WB_cardwrap WB_feed_type S_bg2")
            for r in rs:
                mid = r.get("mid")
                print mid
                if mid in mids or i > 10:
                    flag = False
                    break
                mids.append(mid)
                content = r.find("div", "WB_text W_f14").getText()
                info = r.find("div", "WB_from S_txt2").getText()
                content = recovery(content).encode("gbk")
                info = recovery(info).encode("gbk")
                total.append(dict(content=content, info=info))
                print content, info
            i += 1
    open("d.txt", "w").write(pickle.dumps(total))



while True:
    print "======================================="
    keyword = raw_input("search:").strip()
    if not keyword:
        break

    result = []
    for r in total:
        if keyword in r["content"]:
            result.append(r)

    for r in result:
        print "-----------------------------"
        print r["content"]
        print r["info"]
        print "-----------------------------"



