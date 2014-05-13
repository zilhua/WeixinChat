# coding:UTF-8
import os
import sys
app_root = os.path.dirname(__file__)
sys.path.insert(0,os.path.join(app_root,'beautifulsoup4-4.3.2'))
#sys.path.insert(0, os.path.join(app_root,'beautifulsoup4-4.3.2')
import sae
import web
from weixinInterface import WeixinInterface
urls = (
'/','WeixinInterface',
'/weixin','WeixinInterface'
) 

templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
class Hello:
    def GET(self):
        return render.hello("你好")
app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)