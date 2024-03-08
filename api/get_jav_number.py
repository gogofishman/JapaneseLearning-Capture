import re


def get_jav_number(file_name: str) -> tuple:
    """
    解析番号
    :param file_name:
    :return: (番号，无码，字幕，完整番号)
    """
    jav_number = None
    uncensored = False
    subtitle = False

    match = re.search(r'[a-zA-Z]+-[0-9]+(-[UuCc]+)?', file_name)
    if match:
        jav_number = match.group().upper()

    long_jav_number = jav_number

    if jav_number is not None:
        if jav_number.endswith('-U'):
            uncensored = True
            jav_number = jav_number.replace('-U', '')
        if jav_number.endswith('-C'):
            subtitle = True
            jav_number = jav_number.replace('-C', '')
        if jav_number.endswith('-UC') or jav_number.endswith('-CU'):
            uncensored = True
            subtitle = True
            jav_number = jav_number.replace('-UC', '').replace('-CU', '')

    return jav_number, uncensored, subtitle, long_jav_number
