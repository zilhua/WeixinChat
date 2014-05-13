#coding:UTF-8
import hashlib
import web
import lxml
import time
import os
from lxml import etree
import urllib2,json,urllib
import re
import pylibmc
import random
#import searchZilhua
#from bs4 import BeautifulSoup
#################################
replyContent=u'''大家好，[生物信息]
平台功能正在调试。
有些功能暂时无法
使用，请谅解。
您说的是： '''
replyContentHelp=u'''大家好，[生物信息]
平台功能正在调试。
目前恢复的功能：
1.[搜索@关键字] 
例如输入：
搜索@tophat
可查看与tophat有
关的内容
2.[留言@留言内容]
例如输入：
留言@留言内容
我们即可以收到您
的留言，并尽快处
理您的问题
3.[工具@bwa]
4.输入[小黄鸡]
可以进行人机对话
注意：如果和小黄
鸡对话后，一定要
输入bye才能离开
否者不能使用其他
功能
5.[天气@城市]
例如输入：
天气@武汉
即可查看武汉天气
其他功能正在完善
尽情期待
注意：里面有隐藏
功能哦
'''
#################################
subscribeEvent=u'''感谢您关注[生物信息]
我们的目标：让[菜鸟]
也能进行生物信息
分析让每一台手机也
能当服务器。
输入【帮助】查看使
用方法。'''
guidanceDict={u'天气':u'例如输入[天气@武汉]',
              u'搜索':u'''例如输入
              [搜索@tophat]''',
              u'工具':u'例如输入[工具@bwa]',
              u'留言':u'例如输入[留言@留言内容]'
}
excludeDict={'bye':'have',
             u'拜拜':'have',
             u'拜':'have',
             'byebye':'have',
             u'帮助':'have',
             u'小黄鸡':'have',
             u'黄小鸡':'have',
             'xhj':'have',
             'huangxiaoji':'have',
             'xiaohuangji':'have'
}
pictextTpl = """<xml>
                 <ToUserName><![CDATA[%s]]></ToUserName>
                 <FromUserName><![CDATA[%s]]></FromUserName>
                 <CreateTime>%s</CreateTime>
                 <MsgType><![CDATA[news]]></MsgType>
                 <ArticleCount>1</ArticleCount>
                 <Articles>
                 <item>
                 <Title><![CDATA[%s]]></Title>
                 <Description><![CDATA[%s]]></Description>
                 <PicUrl><![CDATA[%s]]></PicUrl>
                 <Url><![CDATA[%s]]></Url>
                 </item>
                 </Articles>
                 <FuncFlag>1</FuncFlag>
                 </xml> """
################################
class SearchMovies:
    def __int__ (self):
        self.moviesearchbase='http://api.douban.com/v2/movie/search'
        self.moviedetailbase='http://api.douban.com/v2/movie/subject/'
        self.DOUBAN_APIKEY = "0a0038ceff151e561e00aa6cfd3f5b02"  # 这里需要填写你自己在豆瓣上申请的应用的APIKEY
    def searchmovie (self,keywords):
        searchkeys = urllib2.quote(keywords.encode("utf-8"))  # 如果Content中存在汉字，就需要先转码，才能进行请求
        urlsearch = '%s?q=%s&apikey=%s' % (self.moviesearchbase, searchkeys, self.DOUBAN_APIKEY)
        resp = urllib2.urlopen(urllib2.Request(urlsearch))
        movie = json.loads(resp.read())
        return movie
    def detailmovie (self,movie):
        urldetail = '%s%s?apikey=%s' % (self.moviedetailbase, movie["subjects"][0]["id"], self.DOUBAN_APIKEY)
        respdetail = urllib2.urlopen(urllib2.Request(urldetail))
        description = json.loads(respdetail.read())
        description = ''.join(description['summary'])
        return description

class WeatherReport:
    def __init__ (self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    def weatherReport (self,city):
        #读取天气地区,保存为字典
        #req = urllib2.Request()
        city = city.encode('utf-8')
        f=open('weather.txt','r')
        fileContent=f.readlines()
        f.close()
        weatherDict={}
        for eachline in fileContent:
            key = eachline.split(':')[0]
            value=eachline.split(':')[1].rstrip()
            weatherDict[key]=value
        url = '''http://www.weather.com.cn/data/cityinfo/%s.html'''
        if city in weatherDict:
            #return u'北京'
            url= url%(weatherDict[city])
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            reson = json.loads(resp.read())
            #return reson
            return reson
        else:
            return 'NoFound'
        #return u"天气函数"
            
        
    
class XiaoHuangJi:
    def __init__ (self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)        
    def xhjTalk(self,ask): 
        ask = ask.encode('UTF-8')
        enask = urllib2.quote(ask)
        send_headers = {'Cookie':'Filtering=0.0; Filtering=0.0; isFirst=1; isFirst=1; simsimi_uid=50840753; simsimi_uid=50840753; teach_btn_url=talk; teach_btn_url=talk; sid=s%3AzwUdofEDCGbrhxyE0sxhKEkF.1wDJhD%2BASBfDiZdvI%2F16VvgTJO7xJb3ZZYT8yLIHVxw; selected_nc=zh; selected_nc=zh; menuType=web; menuType=web; __utma=119922954.2139724797.1396516513.1396516513.1396703679.3; __utmc=119922954; __utmz=119922954.1396516513.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'}
        baseurl = r'http://www.simsimi.com/func/reqN?lc=zh&ft=0.0&req='
        url = baseurl+enask
        req = urllib2.Request(url,headers=send_headers)
        resp = urllib2.urlopen(req)
        reson = json.loads(resp.read())
        return reson
        #return u'小黄鸡'
    
#打印图文消息
class PrintNews:
    def __init__ (self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)        
    def printNews (self,fromUser,toUser,matchList):
#        return u'okok'
#        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContent+'===='+u'''已经进入printnews函数了''')
#        #微信的消息不能多于十条
        #默认大图片的地址
        BigPicUrl=''
        #默认小图片的地址
        SmallPicUrl=''
        ToUser = fromUser
        FromUser = toUser
        TimeReply = str(int(time.time()))
        arrayLen = len(matchList)
        xmlFormat='''<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%d</ArticleCount>
        <Articles>
        '''
        #xmlFormat=''
        if arrayLen>0:
            #return u'已经进入循环'
            #xmlFormat = %(ToUser,FromUser,TimeReply,arrayLen)
            #返回的顺序 标题，文本链接，描述，图片链接
            arrayLenReply =arrayLen
            if arrayLen>9:
                arrayLenReply = 9
            else:
                arrayLenReply = arrayLen
            xmlFormat = xmlFormat%(ToUser,FromUser,TimeReply,arrayLenReply)
            ##################################################
            for i in range(arrayLen):
                #xmlFormat = xmlFormat + u'A'
                xmlFormat = xmlFormat+matchList[i][0].decode('utf-8')
                xmlFormat +='''
                <item>'''
                #获取标题
                TitleReply = matchList[i][0].decode('utf-8')
                xmlFormat +='''
                <Title><![CDATA[%s]]></Title>'''%(TitleReply)
                #描述
                ScrReply   = matchList[i][2].decode('utf-8')
                xmlFormat +='''
                <Description><![CDATA[%s]]></Description>'''%(ScrReply)
                #图片链接
                PicReply   = matchList[i][3].decode('utf-8')
                if PicReply== u'havenopic':
                    pass
                else:
                    xmlFormat +='''
                    <PicUrl><![CDATA[%s]]></PicUrl>'''%(PicReply)
                #文本链接
                UrlTxtReply= matchList[i][1].decode('utf-8')
                xmlFormat += '''
                <Url><![CDATA[%s]]></Url>'''%(UrlTxtReply)
                xmlFormat += '''
                </item>'''
                if i>=8 :
                    break
                else:
                    continue
            xmlFormat += '''
            </Articles>
            </xml>'''
            return xmlFormat
        else:
            #return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContent+'===='+u'没找到')
            return u'nofound'

            #########
        
#################################
#用于搜索网站:www.zilhua.com
class SearchWebSite:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    def searchweb (self,formKeyWord='tophat'):
        #定义常量
        #网站是utf-8的格式
        searchWebSite='http://www.zilhua.com/?s='+formKeyWord
        searchWebSite=searchWebSite.encode('UTF-8')
        #用于装载所有匹配的信息
        listInfo=[]
#        return searchWebSite
        #下载网站
        response = urllib2.urlopen(searchWebSite)
        html = response.read()
        #hjson = json.loads(html)
        #re.search('Nothing Found',html)
        matchCont= re.compile('<article([\s\S]*?)</article>')
        if matchCont.findall(html):
            for matchRe in matchCont.findall(html):
                #print "ok"
                if re.search(r'Nothing Found',matchRe):
                    #print "no"
                    return "NOpic"
                    #pass
                else:
                    #return 'zhaodaole'
                    listInfo.append(self.TRegExpr(matchRe))
        else:
            pass
        #需要转换编码
        #return listInfo[0][0].decode('utf-8')
        return listInfo
    def TRegExpr(self,matchRe):#返回的顺序 标题，文本链接，描述，图片链接
        #图片默认地址
#        return 'a'
        picWebSite = 'havenopic'
        matchSubList=[]
        #寻找title以及对应的网址
        matchSubTxt = re.compile('<h1[\s\S]*?(<a[\s\S]*?</a>)[\s\S]*?</h1>')
        #matchSubPic = re.compile(<div class="entry-summary">)
        #寻找图片的网址以及对应描述
        matchSubPic = re.compile('<div class\=\"entry-summary\">([\s\S]*?)</div><!-- \.entry-summary -->')
        for matchSub_Re in matchSubTxt.findall(matchRe):
            matchSub_href = re.search (r'<a href=\"(.*)\" title',matchSub_Re)
            matchSub_title= re.search(r'rel\=\"bookmark\">(.*)</a>',matchSub_Re)
            matchSubList.append(str(matchSub_title.group(1)))
            matchSubList.append(str(matchSub_href.group(1)))
        for matchSubPic_Re in matchSubPic.findall(matchRe):
            matchSubPic_href = re.search(r'src\=\"(.*)\" class',matchSubPic_Re)
            matchSubPic_hrefweb= "";
            matchSubPic_p = re.search(r'<p>(.*)</p>' , matchSubPic_Re)
            if matchSubPic_href:
                matchSubPic_hrefweb = matchSubPic_href.group(1)
            else:
                matchSubPic_hrefweb = picWebSite
            matchSubList.append(str(matchSubPic_p.group(1)))
            matchSubList.append(str(matchSubPic_hrefweb))
        return matchSubList
#############################################################################   
class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    def GET(self):
        #获取输入参数
        data=web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="XXXXXX"#请使用自己的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        #sha1加密算法
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            #print "true"
            return echostr
    def POST(self):
        #天气
        weatherReportReply=WeatherReport()
        #查找网站
        searchZilhua=SearchWebSite()
        #小黄鸡
        mcXHJ = pylibmc.Client()
        xhjClass=XiaoHuangJi()
        str_xml=web.data()
        xml=etree.fromstring(str_xml)
        #提取信息
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #渲染模板#
        #判断是否为关注事件
        if msgType =='event':
            return self.render.reply_txt(fromUser,toUser,str(int(time.time())),subscribeEvent)
        else:
            #处理不同种类的消息
            #####文本
            if msgType == 'text':
                content=xml.find("Content").text#
                #文本分段    搜索@tophat  关键词1@关键词2
                #keyWord_search,content_search=content.split('@',1)
                #送给老婆的
                if content==u'我爱大宝':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''老婆 我爱你''')
                if content==u'晚安':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''晚安 愿你永远如此温柔''')
                if content==u'大宝':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''大宝就在你身边''')
                if content==u'我想你':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''大宝就在你身边，让我给你唱一首歌吧''')
                if re.search(u'黑狗',content):
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''哈哈，兽兽是一只大黑狗''')
                if re.search(u'大宝',content) and re.search(u'我想听音乐',content):
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''那让我给我家刘小妞唱一首歌吧''')
                keyWords=content.split('@',1)#
                #return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContent+content+'===='+keyWords[0])
                #功能一：搜索网站内容
                keyWordFirst=keyWords[0]
                keyWordFirst=keyWordFirst.replace('[','')
                keyWordFirst=keyWordFirst.replace(']','')
                keyWordSeconde=''
                if len(keyWords)>=2:
                    keyWordSeconde=keyWords[1]
                    keyWordSeconde=keyWordSeconde.replace('[','')
                    keyWordSeconde=keyWordSeconde.replace(']','')
                if keyWordFirst.strip()=='':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''您的输入有误，试一试输入 搜索@tophat ''')
                elif len(keyWords)<=1 and keyWordFirst.strip()!=u'帮助' and keyWordFirst.strip()!=u'小黄鸡' and keyWordFirst.strip().lower() not in excludeDict:
                    if keyWordFirst.strip() in guidanceDict:
                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''您的输入有误， 
                        '''+guidanceDict[keyWordFirst.strip()]+u'''
                        输入[帮助]查看平台使用说明,输入[小黄鸡]就可以人机对话''')
                    else:
                        #小黄鸡
                        mcxhj = mcXHJ.get(fromUser+'_xhj')
                        if mcxhj == 'xhj':
                            res = xhjClass.xhjTalk(keyWordFirst)
                            if re.search(u'婊子',res['sentence_resp']) or re.search(u'你妈',res['sentence_resp']) or re.search(u'操',res['sentence_resp']) or re.search(u'微信',res['sentence_resp']):
                                #reply_text = u"小黄鸡脑袋出问题了" #这里小黄鸡会有广告
                                return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''小黄鸡脑袋出问题了''')
                            if re.search(u'恭喜',res['sentence_resp']) and  re.search(u'奖',res['sentence_resp']):
                                return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''小黄鸡脑袋出问题了''')
                            if re.search(u'奖',res['sentence_resp']) and re.search(u'中',res['sentence_resp']):
                                return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''小黄鸡脑袋出问题了''')
                            return self.render.reply_txt(fromUser,toUser,str(int(time.time())),res['sentence_resp'])#replyContent+content+u'''  请输入[帮助]查看平台使用方法 输入[小黄鸡]就可以人机对话'''
                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContent+content+u'''  请输入[帮助]查看平台使用方法 输入[小黄鸡]就可以人机对话''')
                elif keyWordFirst.strip() == u'搜索':
                    #peizhihua=searchweb('tophat')
                    #分割需要搜索的关键词 空格都变成+ ，并且判断字符窜长度
                    #return self.render.reply_txt(fromUser,toUser,str(int(time.time())),keyWords[1]+u'''啥情况''')
                    if (len(keyWords[1]))>20:
                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫，您搜索的关键字太长了(不大于20个字)''')
                    else:
                        #将空格转换为'+'号"+".join(s.split())
                        #keyWordSearch = "+".join()
                        keyWordSearch = "+".join(keyWordSeconde.split())
                        searchRe = searchZilhua.searchweb(keyWordSearch)
                        #return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫,貌似木有没找到您说的''')
                        if searchRe == u'NOpic':
                            return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫,貌似木有没找到您说的 ['''+keyWordSeconde+u'''] ,换个关键字在试一下吧,输入帮助查看平台使用方法''')
                        else:
                            printReply = PrintNews()
                            return printReply.printNews(fromUser,toUser,searchRe)
                elif keyWordFirst.strip() == u'留言':
                    return self.render.replyStar_txt(fromUser,toUser,str(int(time.time())),u'''您的留言已收到，我们会尽快处理''')
                elif keyWordFirst.strip()==u'帮助' or keyWordFirst.lower() == u'help':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContentHelp)
                elif keyWordFirst.strip()==u'工具':
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''您好，此部分的内容正在完善中，尽请期待''')
                elif keyWordFirst.strip()==u'小黄鸡' or keyWordFirst.strip().lower()==u'xhj' or keyWordFirst.strip().lower()==u'黄小鸡' or keyWordFirst.strip().lower()=='huangxiaoji' or keyWordFirst.strip().lower()=='xiaohuangji':
                    mcXHJ.set(fromUser+'_xhj','xhj')
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫，您已进入与小黄鸡交谈中，请尽情的蹂躏它吧！注意：输入[bye]才能跳出与小黄鸡的交谈''')
                elif keyWordFirst.strip().lower()==u'bye' or keyWordFirst.strip()==u'拜拜' or keyWordFirst.strip()==u'拜' or keyWordFirst.strip()==u'byebye':
                    mcXHJ.delete(fromUser+'_xhj')
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫，您已退出与小黄鸡交谈中。输入[帮助]查看平台使用说明''')
                elif keyWordFirst.strip()==u'天气':
                    weatherRe = weatherReportReply.weatherReport(keyWordSeconde)
                    if weatherRe == 'NoFound':
                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),u'''主淫，您说的地方找遍整个火星也没找到。输入[帮助]查看平台使用说明''')
                    else:
                        #weatherinfoRe=
                        cityRe=weatherRe['weatherinfo']['city']
                        lowerTem=weatherRe['weatherinfo']['temp1']
                        upTem=weatherRe['weatherinfo']['temp2']
                        weatherRe = weatherRe['weatherinfo']['weather']
                        weatherinfoReply=u'''查询结果如下：
                        城市:%s
                        最低气温:%s
                        最高气温:%s
                        天气:%s'''%(cityRe,lowerTem,upTem,weatherRe)
#                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),weatherinfoReply)
                        return self.render.reply_txt(fromUser,toUser,str(int(time.time())),weatherinfoReply)
                #return self.render.reply_txt(fromUser,toUser,str(int(time.time())),)
                elif keyWordFirst.strip()==u'电影' or keyWordFirst.strip()==u'dianying' or keyWordFirst.strip()==u'dy':
                    moviesinfo=searchmovie(keyWordSeconde)
                    moviedescription=detailmovie(moviesinfo)
                    echostr =pictextTpl % (fromUser,toUser, str(int(time.time())),
                                           moviesinfo["subjects"][0]["title"], moviedescription,
                                           moviesinfo["subjects"][0]["images"]["large"], moviesinfo["subjects"][0]["alt"])
                else:
                    return self.render.reply_txt(fromUser,toUser,str(int(time.time())),replyContent+content+u'''  请输入[帮助]查看平台使用方法''')