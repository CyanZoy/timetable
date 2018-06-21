from django.test import TestCase
import requests
import time
import hashlib

url = 'http://localhost/api?sign={sign}&timestamp={now_time}&doorid={doorid}&appid={appid}&userid={userid}'
now_time = int(time.time())
userid = '1999900109'
doorid = '1211'
appid = 'kb8947539b9ba847b2'

data = {
    'now_time': int(time.time()),
    'userid': '1999900109',
    'doorid': '1211',
    'appid': 'kb8947539b9ba847b2',
}

sortlist = [str(now_time), userid, doorid, appid, '00d6c285b0b7d2fea8afe57a52120aa6']
sortlist.sort()
print('sortlist=', sortlist)
sha = hashlib.sha1()
sha.update(''.join(sortlist).encode('utf-8'))
sign = sha.hexdigest()
data.update({'sign': sign})
print(data)
url = url.format(**data)

con = requests.get(url=url).content
print(con)



