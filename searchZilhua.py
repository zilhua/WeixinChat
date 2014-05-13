# -*- coding:utf-8 -*-
import re
import urllib2
import json

"""
Usage:
    用于搜索自己的网站www.zilhua.com
"""

#接收搜索的关键词
def searchweb (formKeyWord='tophat'):
    #定义常量
    searchWebSite=r'http://www.zilhua.com/?s='+formKeyWord
    searchWebSite = searchWebSite.encode('utf-8')
    txtUrlList=[];
    picUrlList=[]
    titleList=[]
    titleDescriptionList=[]
    listInfo=[]
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
                return listInfo
                #pass
            else:
                listInfo.append(TRegExpr(matchRe))
    else:
        pass
        #return listInfo
    #print listInfo[0][0]
    return listInfo[0][0]
def TRegExpr(matchRe):#返回的顺序 标题，文本链接，描述，图片链接
    #图片默认地址
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
        #print matchSub_href.group(1),'======',matchSub_title.group(1)
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
        #print matchSubPic_p.group(1),'+++++++++++',matchSubPic_hrefweb
    return matchSubList

print searchweb(u'文章')