import json
import os

from yolib import Helper


class Data:
    """data数据类"""

    _dict: dict = {
        'actor_img_url': {},
    }

    def __init__(self):
        Helper.logging.debug('开始加载data数据文件...')

        # 检查文件是否存在
        if not os.path.exists("data\\data.json"):
            self._write()

            Helper.logging.debug('找不到data.json文件，已新建json文件')

        with open('data\\data.json', 'r', encoding='utf-8') as f:
            self._dict = json.load(f)

    def _write(self):
        with open('data\\data.json', 'w', encoding='utf-8') as f:
            json.dump(self._dict, f, ensure_ascii=False, indent=2)

    def get_actor_img_url(self, actor_name: str) -> str | None:
        """获取data数据中演员图片链接"""
        return self._dict['actor_img_url'].get(actor_name)

    def add_actor_img_url(self, actor_name: str, img_url: str):
        """添加演员图片链接到data数据"""
        self._dict['actor_img_url'][actor_name] = img_url
        self._write()
        Helper.logging.debug(f'添加演员"{actor_name}"的图片链接到data数据中')


data = Data()
