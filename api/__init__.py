# 前后端通信api
import os
import importlib
from types import ModuleType

import scraper
from scraper import BaseScraper
from .config import Config
from .get_jav_number import get_jav_number
from .videoClass import Video
from .debug import logging


class Api(Config):
    video_format: tuple = ('.mp4', '.mkv', '.avi', '.rmvb', '.flv', '.mov', '.rm', '.wvm')
    module_list: dict[str, ModuleType] = {}
    """保存所有刮削器的文件模块字典"""

    def __init__(self):
        super().__init__()

        # 加载全部Scraper文件
        path = os.path.dirname(__file__).replace('api', 'scraper')

        for file in os.listdir(path):
            if not file.endswith('.py') or file == '__init__.py':
                continue

            module = importlib.import_module(f'scraper.{file[:-3]}')

            # 检查模块是否含Scraper类
            try:
                instance = module.Scraper()
                instance = None
            except Exception:
                continue

            Api.module_list[file[:-3]] = module
            logging.debug(f'加载刮削器 "{file[:-3]}" 成功!')

    def search_file(self) -> dict:
        """查找文件"""

        path = self.input_path()

        if not os.path.exists(path) or path.startswith(("\\", "/")):
            return {}

        video_dict = {}
        for file in os.listdir(path):

            file_path = os.path.join(path, file)

            if not file.endswith(Api.video_format):
                continue
            size = os.stat(file_path).st_size / (1024 ** 2)

            if self.ignore_100mb() == 'True':
                if size < 100:
                    continue

            # 解析番号
            jav_number = get_jav_number(file)
            video_dict[file] = {
                "path": file_path,
                "size": size / 1024,
                "jav_number": jav_number[0],
                "uncensored": jav_number[1],
                "subtitle": jav_number[2],
                "long_jav_number": jav_number[3]
            }
        return video_dict

    def scraper_run(self, video_title: str, file_path: str, _type: str = 'JavDB') -> int:
        """
        开始刮削
        :param video_title:
        :param file_path:
        :param _type:
        :return: 0 成功 ，-1 失败 ，1 有误
        """

        def log(text):
            logging.log(f'[{_type}] [{video_title}] {text}')

        def warning(text):
            logging.warning(f'[{_type}] [{video_title}] {text}')

        def error(text):
            logging.error(f'[{_type}] [{video_title}] {text}')

        mistaken = False
        video = Video()

        scraper_instance: BaseScraper = self.module_list[_type].Scraper()

        log('开始刮削...')

        # 搜索影片首页
        webpage = scraper_instance.search_video_page(video_title)
        if webpage is None:
            error('无法搜索到影片网页！该影片刮削结束！')
            return -1
        log('已搜索到影片网页')

        # 解析标题
        re = scraper_instance.parse_title(webpage)
        if re is None:
            mistaken = True
            warning('解析标题失败')
        else:
            video.title, video.originaltitle, video.sorttitle, video.num = re
            video.title = video.title.strip()
            video.originaltitle = video.originaltitle.strip()
            video.sorttitle = video.sorttitle.strip()
            video.num = video.num.strip()
            log('已解析标题')

        # 解析评分
        re = scraper_instance.parse_rating(webpage)
        if re is None:
            mistaken = True
            warning('解析评分、分级失败')
        else:
            video.mpaa, video.rating = re
            video.customrating = video.mpaa
            log('已解析评分、分级')

        # 解析导演
        re = scraper_instance.parse_director(webpage)
        if re is None:
            mistaken = True
            warning('解析导演失败')
        else:
            video.director = re
            log('已解析导演')

        # 解析演员
        re = scraper_instance.parse_actor(webpage)
        if re is None:
            mistaken = True
            warning('解析演员失败')
        else:
            video.actor = re
            log('已解析演员')

        # 解析制作商
        re = scraper_instance.parse_studio(webpage)
        if re is None:
            mistaken = True
            warning('解析制作商失败')
        else:
            video.studio, video.maker = re
            log('已解析制作商')

        # 解析特征
        re = scraper_instance.parse_feature(webpage)
        if re is None:
            mistaken = True
            warning('解析系列和简介失败')
        else:
            video.set, video.plot = re
            log('已解析系列和简介')

        # 解析标签
        re = scraper_instance.parse_tag(webpage)
        if re is None:
            mistaken = True
            warning('解析标签失败')
        else:
            video.tag = re
            log('已解析标签')

        # 解析类型
        re = scraper_instance.parse_genre(webpage, video.tag)
        if re is None:
            mistaken = True
            warning('解析风格类型失败')
        else:
            video.genre = re
            log('已解析风格类型')

        # 解析年份
        re = scraper_instance.parse_date(webpage)
        if re is None:
            mistaken = True
            warning('解析时间年份失败')
        else:
            year, releasedate = re
            video.year = year
            video.releasedate = releasedate
            video.release = releasedate
            video.premiered = releasedate
            log('已解析时间年份')

        # 创建目录
        output_path = scraper_instance.parse_directory(api.output_path(), video)
        os.makedirs(output_path, exist_ok=True)
        log(f'创建影片文件夹成功：{output_path}')

        extrafanart_path = f'{output_path}/extrafanart'
        os.makedirs(extrafanart_path, exist_ok=True)
        log(f'创建剧照文件夹成功：{extrafanart_path}')

        # 下载图片
        re = scraper_instance.download_photo(webpage, output_path, extrafanart_path)
        if re is False:
            error('下载图片失败！该影片刮削结束！')
            return -1
        log('已下载图片')

        # 移动文件，创建info文件
        re = scraper_instance.move_file(video, file_path, output_path, video.title)
        if re is False:
            error('移动视频文件失败！该影片刮削结束！')
            return -1
        log('已移动视频文件，并创建info文件')

        if mistaken:
            return 1

        return 0

    def test_translate(self, text):
        return scraper.translator.translate(text)


api = Api()
