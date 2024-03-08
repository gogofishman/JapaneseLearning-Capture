import opencc
import re

from api.debug import logging
from .google import translate_google
from .tencent import translate_tencent
from .baidu import translate_baidu


class Translator:
    translate_on = True
    translate_engine = 'google'
    """['google', 'baidu', 'tencent']"""

    translate_target = "zh"

    tencent_api = {
        'id': '',
        'key': ''
    }
    baidu_api = {
        'id': '',
        'key': ''
    }

    @staticmethod
    def traditional_to_simplified(text: str) -> str | None:
        """繁体中文转简体中文，不使用云端翻译"""
        try:
            converter = opencc.OpenCC('t2s.json')
            result = converter.convert(text)
            return result.strip()
        except Exception:
            logging.debug(f'繁化简翻译失败！文本：{text}')
            return None

    @staticmethod
    def simplified_to_traditional(text: str) -> str | None:
        """简体中文转繁体中文，不使用云端翻译"""
        try:
            converter = opencc.OpenCC('s2t.json')
            result = converter.convert(text)
            return result.strip()
        except Exception:
            logging.debug(f'简化繁翻译失败！文本：{text}')
            return None

    def translate(self, text: str) -> str | None:
        """云翻译翻译"""

        if self.translate_on is False:
            return text

        target_language = self.translate_target

        # 谷歌翻译
        if self.translate_engine == 'google':
            target_language = 'zh-TW' if target_language == 'cht' else target_language
            target_language = 'ko' if target_language == 'kor' else target_language
            target_language = 'fr' if target_language == 'fra' else target_language
            target_language = 'zh-cn' if target_language == 'zh' else target_language

            return translate_google(text, target_language)

        # 百度翻译
        if self.translate_engine == 'baidu':
            id_ = self.baidu_api['id']
            key = self.baidu_api['key']

            return translate_baidu(text, id_, key, target_language)

        # 腾讯翻译
        if self.translate_engine == 'tencent':
            id_ = self.tencent_api['id']
            key = self.tencent_api['key']

            target_language = 'zh-TW' if target_language == 'cht' else target_language
            target_language = 'ko' if target_language == 'kor' else target_language
            target_language = 'fr' if target_language == 'fra' else target_language

            return translate_tencent(text, id_, key, target_language)

    def translate_split(self, text: str, split_patterns: tuple = (r"[ ]{2,}", r"[\n]{1,}")) -> str | None:
        """
        拆分文本并翻译
        :param text: 翻译文本
        :param split_patterns: 用作拆分的字符，为正则表达式 （默认参数表示2个及以上的空格或1一个及以上的换行符作为分割字符）
        :return: 返回翻译后的文本，同时保留原有的拆分字符不变
        """

        if self.translate_on is False:
            return text

        # 拆分文本
        split_list = []

        for pattern in split_patterns:
            all_matches = re.finditer(pattern, text)
            for match in all_matches:
                start = match.start()
                end = match.end()
                split_list.append((start, end))

        split_list.sort(key=lambda x: x[0])

        # 整理拆分后的文本
        text_list = []

        for i in range(len(split_list)):
            if i == len(split_list) - 1:
                text_list.append(split_list[i])
                break

            last = split_list[i]
            next_ = split_list[i + 1]

            if last[1] == next_[0]:
                text_list.append(last)
            else:
                text_list.append(last)
                text_list.append([last[1], next_[0]])

        if text_list[0][0] != 0:
            text_list.insert(0, [0, text_list[0][0]])
        if text_list[-1][1] != len(text):
            text_list.append([text_list[-1][1], len(text)])

        # 翻译文本
        result_list = []

        for i in text_list:
            if isinstance(i, list):
                source_text = text[i[0]:i[1]]
                result = self.translate(source_text)

                if result is None:
                    return None

                result_list.append(result)
            else:
                result_list.append(text[i[0]:i[1]])

        return ''.join(result_list)


translator = Translator()
