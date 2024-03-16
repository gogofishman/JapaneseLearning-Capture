# 配置文件相关
import json
import os

import scraper
from yolib import Helper


class Config:
    """一个配置文件类，赋值时会自动写入ini文件中"""

    def __init__(self):

        self._select_scraper = 'JavDB'
        self._check_update = True
        self._ignore_100mb = True
        self._input_path = ""
        self._output_path = "JAV"
        self._connect_timeout = 15
        self._connect_reconnections = 3
        self._connect_sleep = 3
        self._proxy_on = True
        self._proxy_host = "127.0.0.1"
        self._proxy_port = "7890"

        self._translate = {
            "on": False,
            "engine": 'google',
            "target": "zh",
            "tencent": {
                "id": "",
                "key": ""
            },
            "baidu": {
                "id": "",
                "key": ""
            }
        }

    def config_init(self):
        Helper.logging.debug('开始加载ini配置文件...')
        self._read()
        self._write()

    def _write(self):
        with open('data\\config.json', 'w', encoding='utf-8') as f:
            dict_ = {key[1:]: value for key, value in self.__dict__.items() if key[0] == '_'}
            json.dump(dict_, f, ensure_ascii=False, indent=2)

        # 更新Session配置
        proxy = {
            'http': f'http://{self.proxy_host()}:{self.proxy_port()}',
            'https': f'http://{self.proxy_host()}:{self.proxy_port()}'
        }
        if self.proxy_on():
            scraper.session.proxies = proxy
        else:
            scraper.session.proxies = ''
        scraper.session.timeout = self.connect_timeout()
        scraper.session.connect_reconnections = self.connect_reconnections()
        scraper.session.connect_sleep = self.connect_sleep()

        # 更新翻译配置
        scraper.translator.translate_on = self.translate_on()
        scraper.translator.translate_engine = self.translate_engine()
        scraper.translator.translate_target = self.translate_target()
        scraper.translator.tencent_api = {
            'id': self.translate_tencent_id(),
            'key': self.translate_tencent_key()
        }
        scraper.translator.baidu_api = {
            'id': self.translate_baidu_id(),
            'key': self.translate_baidu_key()
        }

        Helper.logging.debug('写入config.json配置文件成功')

    def _read(self):
        # 检查文件是否存在
        if not os.path.exists("data\\config.json"):
            self._write()
            Helper.logging.debug('找不到配置文件，已新建config.json文件')

        with open('data\\config.json', 'r', encoding='utf-8') as f:
            dict_ = json.load(f)
            for i in dict_:
                if "_" + i in self.__dict__:
                    self.__dict__["_" + i] = dict_[i]

    # 使用函数来模拟get和set方便前端js直接调用

    def select_scraper(self, value=None):
        if value is None:
            return self._select_scraper
        else:
            self._select_scraper = value
            self._write()

    def check_update(self, value=None):
        if value is None:
            return self._check_update
        else:
            self._check_update = value
            self._write()

    def ignore_100mb(self, value=None):
        if value is None:
            return self._ignore_100mb
        else:
            self._ignore_100mb = value
            self._write()

    def input_path(self, value=None):
        if value is None:
            if self._input_path == "":
                self._input_path = os.getcwd()
                self._write()
            return self._input_path
        else:
            if value == "":
                value = os.getcwd()
            self._input_path = value
            self._write()
            return self._input_path

    def output_path(self, value=None):
        if value is None:
            return self._output_path
        else:
            self._output_path = value
            self._write()

    def connect_timeout(self, value=None):
        if value is None:
            return self._connect_timeout
        else:
            self._connect_timeout = value
            self._write()

    def connect_reconnections(self, value=None):
        if value is None:
            return self._connect_reconnections
        else:
            self._connect_reconnections = value
            self._write()

    def connect_sleep(self, value=None):
        if value is None:
            return self._connect_sleep
        else:
            self._connect_sleep = value
            self._write()

    def proxy_on(self, value=None):
        if value is None:
            return self._proxy_on
        else:
            self._proxy_on = value
            self._write()

    def proxy_host(self, value=None):
        if value is None:
            return self._proxy_host
        else:
            self._proxy_host = value
            self._write()

    def proxy_port(self, value=None):
        if value is None:
            return self._proxy_port
        else:
            self._proxy_port = value
            self._write()

    def translate_on(self, value=None):
        if value is None:
            return self._translate['on']
        else:
            self._translate['on'] = value
            self._write()

    def translate_engine(self, value=None):
        if value is None:
            return self._translate['engine']
        else:
            self._translate['engine'] = value
            self._write()

    def translate_target(self, value=None):
        if value is None:
            return self._translate['target']
        else:
            self._translate['target'] = value
            self._write()

    def translate_tencent_id(self, value=None):
        if value is None:
            return self._translate['tencent']['id']
        else:
            self._translate['tencent']['id'] = value
            self._write()

    def translate_tencent_key(self, value=None):
        if value is None:
            return self._translate['tencent']['key']
        else:
            self._translate['tencent']['key'] = value
            self._write()

    def translate_baidu_id(self, value=None):
        if value is None:
            return self._translate['baidu']['id']
        else:
            self._translate['baidu']['id'] = value
            self._write()

    def translate_baidu_key(self, value=None):
        if value is None:
            return self._translate['baidu']['key']
        else:
            self._translate['baidu']['key'] = value
            self._write()
