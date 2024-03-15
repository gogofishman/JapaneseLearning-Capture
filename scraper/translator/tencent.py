import hmac
import base64
import random
import time
import hashlib
import requests
import json

from urllib.parse import quote

from yolib import Helper


def _tencent_get_url_encoded_params(text, id_, key, target_language):
    action = 'TextTranslate'
    region = 'ap-shanghai'
    timestamp = int(time.time())
    nonce = random.randint(1, 1e6)
    secret_id = id_
    secret_key = key
    version = '2018-03-21'
    lang_from = 'auto'
    lang_to = target_language

    params_dict = {
        # 公共参数
        'Action': action,
        'Region': region,
        'Timestamp': timestamp,
        'Nonce': nonce,
        'SecretId': secret_id,
        'Version': version,
        # 接口参数
        'ProjectId': 0,
        'Source': lang_from,
        'Target': lang_to,
        'SourceText': text
    }
    params_str = ''
    for key in sorted(params_dict.keys()):
        pair = '='.join([key, str(params_dict[key])])
        params_str += pair + '&'
    params_str = params_str[:-1]
    signature_raw = 'GETtmt.tencentcloudapi.com/?' + params_str
    hmac_code = hmac.new(bytes(secret_key, 'utf8'), signature_raw.encode('utf8'), hashlib.sha1).digest()
    sign = quote(base64.b64encode(hmac_code))
    params_dict['Signature'] = sign
    temp_list = []
    for k, v in params_dict.items():
        temp_list.append(str(k) + '=' + str(v))
    params_data = '&'.join(temp_list)
    return params_data


def translate_tencent(text, id_, key, target_language='zh'):
    try:
        url_with_args = 'https://tmt.tencentcloudapi.com/?' + _tencent_get_url_encoded_params(text, id_, key,
                                                                                              target_language)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36'
        }
        res = requests.get(url_with_args, headers=headers)
        json_res = json.loads(res.text)
        trans_text = json_res['Response']['TargetText']
        return trans_text
    except Exception:
        Helper.logging.debug(f'tencent翻译失败！文本：{text}')
        return None
