import hashlib
import json
import requests
import random

from yolib import Helper


class BaiduFanyi:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        endpoint = 'https://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        self.url = endpoint + path

    @staticmethod
    def _make_md5(s, encoding='utf-8'):
        return hashlib.md5(s.encode(encoding)).hexdigest()

    def translate(self, text, toLang="zh"):
        query = text
        salt = random.randint(32768, 65536)
        sign = self._make_md5(self.appid + query
                              + str(salt) + self.appkey)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appid, 'q': query, 'from': "auto",
                   'to': toLang, 'salt': salt, 'sign': sign}

        r = requests.post(self.url, params=payload, headers=headers)
        result_json = json.loads(r.text)
        result_list = []

        if 'error_code' in result_json:
            return result_json['error_msg']
        else:
            for result in result_json["trans_result"]:
                result_list.append(result['dst'])
            return "\n".join(result_list)


def translate_baidu(text, id_, key, target_language='zh'):
    try:
        BaiduTranslate_test = BaiduFanyi(id_, key)
        Results = BaiduTranslate_test.translate(text, target_language)
        return Results
    except Exception:
        Helper.logging.debug(f'百度翻译失败！文本：{text}')
        return None
