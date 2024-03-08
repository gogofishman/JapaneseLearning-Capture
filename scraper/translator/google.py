import googletrans

from api.debug import logging


def translate_google(text: str, target_language='zh'):
    try:
        google_trans = googletrans.Translator()
        result = google_trans.translate(text, dest=target_language).text
        return result
    except Exception:
        logging.debug(f'google翻译失败！文本：{text}')
        return None
