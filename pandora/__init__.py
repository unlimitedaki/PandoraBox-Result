from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
import os
import urllib.request
import base64
import json
import hashlib

def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    return text

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
        """
        **请使用 PIL 进行本函数的编写**
        获取请求的 query_string 中携带的 b64_url 值
        从 b64_url 下载一张图片的 base64 编码，reshape 转为 100*100，并开启抗锯齿（ANTIALIAS）
        对 reshape 后的图片分别使用 base64 与 md5 进行编码，以 JSON 格式返回，参数与返回格式如下
        
        :param: b64_url: 
            本题的 b64_url 以 arguments 的形式给出，可能会出现两种输入
            1. 一个 HTTP URL，指向一张 PNG 图片的 base64 编码结果
            2. 一个 TXT 文本文件的文件名，该 TXT 文本文件包含一张 PNG 图片的 base64 编码结果
                此 TXT 需要通过 SSH 从服务器中获取，并下载到`pandora`文件夹下，具体请参考挑战说明
        
        :return: JSON
        {
            "md5": <图片reshape后的md5编码: str>,
            "base64_picture": <图片reshape后的base64编码: str>
        }
        """
        pass

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

