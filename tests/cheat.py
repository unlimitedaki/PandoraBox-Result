import re
import urllib.request
import json

re_expr = '<tr>\n<td.+>(.+)</td>\n<td.+>(.+)</a></td>\n<td.+>(.+)</td>\n<td.+>(.+)</td>\n.+\n</tr>'

def download_file(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    return text

data = download_file('https://github.com/996icu/996.ICU/blob/master/blacklist/README.md')
re_cmp = re.compile(re_expr)
result = re_cmp.findall(data)
ret = []
for i in result:
    ret.append({
        'city':i[0],
        'company':i[1],
        'exposure_time':i[2],
        'description':i[3]
    })
print(json.dumps(ret))