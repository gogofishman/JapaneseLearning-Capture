# 自定义刮削器放在同目录下，类名命名为Scraper
import os
import shutil

from abc import ABC, abstractmethod

from api.videoClass import Video, nfoClass
from .data import data
from .request import session
from .translator import translator
from .img import image_editor


class BaseScraper(ABC):
    """刮削器基类"""

    _session = session
    _translator = translator
    _image_editor = image_editor
    _data = data

    @property
    def session(self):
        """返回重写过的requests的Session实例，用于http访问

        自动配置了get、post方法的代理、超时、重连次数、连接间隔等网络连接设置
        """
        return self._session

    @property
    def translator(self):
        """返回翻译器实例"""
        return self._translator

    @property
    def image_editor(self):
        """返回图片编辑器实例"""
        return self._image_editor

    @property
    def data(self):
        """返回data数据类实例"""
        return self._data

    @abstractmethod
    def check_connect(self) -> bool:
        """
        检查刮削器用到的网站是否都能成功连接
        :return: 成功返回True，否则返回False
        """

    @abstractmethod
    def search_video_page(self, video_title: str) -> str | dict[str, str] | None:
        """
        搜索影片首页，返回网页文本，失败返回None
        :param video_title: 
        :return: 返回一个或多个网页(多个网页用于应对不同信息从多个网页上获取的情况,其他函数参数均为该字典,字典key根据自己需要自定义)
        """

    @abstractmethod
    def parse_title(self, web_page: str | dict[str, str]) -> tuple[str, str, str, str] | None:
        """
        解析标题，返回一个元组，依次包含主标题，原标题，短标题和编号，失败返回None
        :param web_page: 影片网页文本
        :return: (title、originaltitle、sorttitle、num)
        """

    @abstractmethod
    def parse_rating(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        """
        解析评级，返回一个元组，依次包含分级和评分（尽量以10为满分），失败返回None
        :param web_page: 影片网页文本
        :return: (mpaa、rating)
        """

    @abstractmethod
    def parse_director(self, web_page: str | dict[str, str]) -> str | None:
        """
        解析导演，返回导演名字，失败返回None
        :param web_page: 影片网页文本
        :return: director
        """

    @abstractmethod
    def parse_actor(self, web_page: str | dict[str, str]) -> list[tuple[str, str, str]] | None:
        """
        解析演员，返回一个包含元组的list，list每个元素对应一组演员元组，元组依次包含演员名字、照片链接和性别，失败返回None
        :param web_page: 影片网页文本
        :return: [(actor1, thumb_url1, sex1), (actor2, thumb_url2, sex2), ...]
        """

    @abstractmethod
    def parse_studio(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        """
        解析发行商和制片方，返回一个元组，依次包含发行商和制片方，失败返回None
        :param web_page: 影片网页文本
        :return: (studio、maker)
        """

    @abstractmethod
    def parse_feature(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        """
        解析特征，返回一个元组，依次包含影片系列和简介，失败返回None
        :param web_page: 影片网页文本
        :return: (set、plot)
        """

    @abstractmethod
    def parse_tag(self, web_page: str | dict[str, str]) -> list[str] | None:
        """
        解析标签，返回一个list，list每个元素对应一个标签，失败返回None
        :param web_page: 影片网页文本
        :return: [tag1, tag2, ...]
        """

    @abstractmethod
    def parse_genre(self, web_page: str | dict[str, str], tag: list[str] | None) -> list[str] | None:
        """
        解析类型，返回一个list，list每个元素对应一个类型，失败返回None
        :param tag: 上一个方法解析得到的标签，也可以用作风格
        :param web_page: 影片网页文本
        :return: [genre1, genre2, ...]
        """

    @abstractmethod
    def parse_date(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        """
        解析发行年月日，返回一个元组，依次包含年份和上映日期，失败返回None
        :param web_page: 影片网页文本
        :return: (year、releasedate)
        """

    @abstractmethod
    def download_photo(self,
                       web_page: str | dict[str, str],
                       photo_path: str,
                       extrafanart_path: str) -> bool:
        """
        解析图片并下载，包含海报、缩略图、fanart和剧照，成功返回True，失败返回False
        :param web_page: 影片网页文本
        :param photo_path: 保存海报、缩略图、fanart的地址
        :param extrafanart_path: 保存剧照的地址
        """

    @staticmethod
    def parse_directory(output_path: str, video: Video) -> str:
        """
        返回具体影片的输出目录，该目录应包含媒体文件，nfo文件，图片文件\n
        (子类如需采用不同的输出目录结构可覆写)
        """
        path = f'{output_path}/{",".join(video.get_actor_list())}/{video.title}'
        return path

    @staticmethod
    def move_file(video: Video, file_path: str, output_path: str, output_title: str, output_title_suffix: str) -> bool:
        """
        移动文件到输出目录，同时创建nfo文件，成功返回True，失败返回False
        """

        def get_file_extension(file):
            _, extension = os.path.splitext(file)
            return extension

        try:
            # 移动文件
            shutil.move(file_path, f'{output_path}/{output_title}{output_title_suffix}{get_file_extension(file_path)}')

            # 创建nfo文件
            nfo = nfoClass.Nfo(video, f'{output_path}/{output_title}{output_title_suffix}.nfo')
            nfo.save()

            return True
        except Exception:
            return False
