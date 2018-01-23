import urllib.request
import re
import time
import urllib.error


#设定一个函数，功能是使用代理服务器爬取数据
def use_proxy(proxy_addr,url):

    #建立异常处理机制
    try:

        #将url设置为请求
        req = urllib.request.Request(url)
        #给请求添加头部，使爬虫伪装成浏览器
        req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0")
        #设置代理
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(req).read()
        return data
    #异常处理
    except urllib.error.URLError as e:
        if hasattr (e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

        #若URLError异常，延迟10秒
        time.sleep(10)

    except Exception as e:
            print("exception:" + str(e))

            #若为Exception异常，延迟1秒
            time.sleep(1)


#设置搜索关键词
keyword = "python"

#设置代理服务器，若此服务器失效，再更换其他服务器
proxy_addr = "10.5.215.56"

#设置爬的页数
for i in range(1,8):

    #将搜索词转码
    key = urllib.request.quote(keyword)
    thispageurl = "http://weixin.sogou.com/weixin?query="+ keyword +"&_sug_type_=&sut=3578&lkt=7%2C1516670349013%2C1516670352605&s_from=input&_sug_=y&type=2&sst0=1516670352708&page="+ str(i) + "&ie=utf8&w=01019900&dr=1"
    thispagedata = use_proxy(proxy_addr,thispageurl)

    #测试是否爬取到数据
    print(len(str(thispagedata)))

    #利用正则表达式进行文章地址采集
    pat1 = 'a target="_blank" href="(.*?)" '
    results = re.compile(pat1,re.S).findall(str(thispagedata))

    #测试是否匹配到文章URL
    print(len(results))

    if(len(results)==0):
        print("第" + str(i) + "爬取失败")
        continue
    
    for j in range(0,len(results)):
        thisurl=results[j]

        #由于采集到的网址中带有"amp;",浏览器无法访问，将"amp;"替换掉
        thisurl=thisurl.replace("amp;","")

        #设置本地目录，爬取数据
        file="/Users/Rocky1/Desktop/weixinArticle/"+"第"+str(i)+"页第"+str(j)+"篇文章.html"
        thisdata=use_proxy(proxy_addr,thisurl)
        try:
            fh=open(file,"wb")
            fh.write(thisdata)
            fh.close()
            print("第"+ str(i) +"页第"+str(j)+"篇成功。")
        except Exception as e:
            print(e)
            print("第"+ str(i) +"页第"+str(j)+"篇失败。")
            
        
        
    



