import os
from multiprocessing import Queue

from .debug import logging
from .videoClass import Video
from scraper import BaseScraper


def scraper_run(queue: Queue, self, video_title: str, video_title_suffix: str, file_path: str, scraper: str = 'JavDB'):
    def log(text):
        logging.log(f'[{scraper}] [{video_title}] {text}')

    def warning(text):
        logging.warning(f'[{scraper}] [{video_title}] {text}')

    def error(text):
        logging.error(f'[{scraper}] [{video_title}] {text}')

    mistaken = False
    video = Video()
    video.scraper = scraper

    scraper_instance: BaseScraper = self.module_list[scraper].Scraper()

    log('开始刮削...')

    # 搜索影片首页
    webpage = scraper_instance.search_video_page(video_title)
    if webpage is None:
        error('无法搜索到影片网页！该影片刮削结束！')
        queue.put(-1)
        return
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
    output_path = scraper_instance.parse_directory(self.output_path(), video)
    os.makedirs(output_path, exist_ok=True)
    log(f'创建影片文件夹成功：{output_path}')

    extrafanart_path = f'{output_path}/extrafanart'
    os.makedirs(extrafanart_path, exist_ok=True)
    log(f'创建剧照文件夹成功：{extrafanart_path}')

    # 下载图片
    re = scraper_instance.download_photo(webpage, output_path, extrafanart_path)
    if re is False:
        error('下载图片失败！该影片刮削结束！')
        queue.put(-1)
        return
    log('已下载图片')

    # 移动文件，创建info文件
    re = scraper_instance.move_file(video, file_path, output_path, video.title, video_title_suffix)
    if re is False:
        error('移动视频文件失败！该影片刮削结束！')
        queue.put(-1)
        return
    log('已移动视频文件，并创建info文件')

    if mistaken:
        queue.put(1)
        return

    queue.put(0)
