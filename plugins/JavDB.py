import re

from scraper import BaseScraper
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://javdb.com/',
}
cookie = {
    'over18': '1',
    'locale': 'zh'
}
web_page_url = ''
sorttitle = ''
jav_number = ''


def get_info(web_page, key: str, text: bool = True):
    soup = BeautifulSoup(web_page, 'lxml')
    info_div = soup.find('nav', class_='panel movie-panel-info')

    for div in info_div.findAll('div', class_='panel-block'):
        if key in div.text:
            if text:
                return div.find('span', class_='value').text
            else:
                return div.find('span', class_='value')

    return None


class Scraper(BaseScraper):
    """JavDB刮削器"""

    def document(self) -> str:
        pass

    def check_connect(self) -> bool:
        pass

    def search_video_page(self, video_title: str) -> str | dict[str, str] | None:

        # 访问搜索界面
        search_url = f'https://javdb.com/search?q={video_title}&f=all'
        response = self.session.get(search_url, headers=headers, cookies=cookie)
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            a = soup.find('a', class_='box')
            jav_number = a.find('div', class_='video-title').find('strong').text

            if video_title in jav_number or jav_number in video_title:
                # 访问影片界面
                href = f"https://javdb.com{a['href']}"
                global web_page_url
                web_page_url = href

                headers['Referer'] = search_url
                response = self.session.get(href, headers=headers, cookies=cookie)
                return response.text

        except Exception:
            return None

        return None

    def parse_title(self, web_page: str | dict[str, str]) -> tuple[str, str, str, str] | None:
        soup = BeautifulSoup(web_page, 'lxml')

        try:
            h2 = soup.find('h2', class_='title')
            strong = h2.findAll('strong')

            num = strong[0].text
            global sorttitle
            sorttitle = strong[1].text
            title = num
            originaltitle = f'{num} {sorttitle}'

            global jav_number
            jav_number = num

            return title, originaltitle, sorttitle, num
        except Exception:
            return None

    def parse_rating(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        try:
            rating = get_info(web_page, '評分')
            if rating is None:
                return None

            rating = re.search(r'[\d.]+', rating).group()
            return 'JP-18+', str(float(rating) * 2)

        except Exception:
            return None

    def parse_director(self, web_page: str | dict[str, str]) -> str | None:
        try:
            director = get_info(web_page, '導演')
            if director is None:
                return ""

            return director

        except Exception:
            return None

    def parse_actor(self, web_page: str | dict[str, str]) -> list[tuple[str, str, str]] | None:
        actors = []

        try:
            soup = BeautifulSoup(web_page, 'lxml')
            info_div = soup.find('nav', class_='panel movie-panel-info')

            for div in info_div.findAll('div', class_='panel-block'):
                if '演員' in div.text:
                    list = div.find('span', class_='value')

                    names_list = [a.text for a in list.findAll('a')]
                    url_list = [a['href'] for a in list.findAll('a')]
                    gender_list = ['female' if '♀' in strong.text else 'male' for strong in list.findAll('strong')]

                    # 获取演员头像链接
                    for index, url in enumerate(url_list):
                        # 从data数据中寻找是否已含有
                        _url = self.data.get_actor_img_url(names_list[index])
                        if _url is not None:
                            url_list[index] = _url
                            continue

                        # 否则重新搜索并添加到data
                        headers['Referer'] = web_page_url
                        response = self.session.get(f"https://javdb.com{url}", headers=headers, cookies=cookie)
                        soup = BeautifulSoup(response.text, 'lxml')

                        img_div = soup.find('div', class_='column actor-avatar')
                        if img_div is None:
                            continue

                        img_url = re.findall(r'url\((.*?)\)', img_div.prettify())[0]

                        url_list[index] = img_url
                        self.data.add_actor_img_url(names_list[index], img_url)

                    # 生成演员列表
                    for index, name in enumerate(names_list):
                        actors.append((name, url_list[index], gender_list[index]))

                    return actors
        except Exception:
            return None
        return None

    def parse_studio(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        studio = ''
        maker = ''

        try:
            _studio = get_info(web_page, '發行')
            if _studio is not None:
                studio = _studio

            _maker = get_info(web_page, '片商')
            if _maker is not None:
                maker = _maker

            # 如果有一个为空，则两个都为不为空的值
            if studio == '' and maker != '':
                studio = maker
            elif studio != '' and maker == '':
                maker = studio

            return studio, maker

        except Exception:
            return None

    def parse_feature(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        set_ = ''

        try:
            _set = get_info(web_page, '系列')
            if _set is not None:
                set_ = _set

            # 将标题翻译为简介
            plot = self.translator.translate_split(sorttitle, split_patterns=(r"[ ]{1,}", r"[\n]{1,}"))
            if plot is None:
                plot = sorttitle

            return set_, plot

        except Exception:
            return None

    def parse_tag(self, web_page: str | dict[str, str]) -> list[str] | None:
        try:
            div = get_info(web_page, '類別', False)
            tag_divs = div.findAll('a')
            tag = [i.text for i in tag_divs]

            # 将标签简体化
            if self.translator.translate_target == 'zh':
                tag = [self.translator.traditional_to_simplified(i) for i in tag]

            if tag is None:
                return None

            return tag

        except Exception as e:
            return None

    def parse_genre(self, web_page: str | dict[str, str], tag: list[str] | None) -> list[str] | None:
        try:
            re_ = []
            set_ = get_info(web_page, '系列')

            if tag is not None:
                re_.extend(tag)
            if set_ is not None:
                re_.append(set_)

            return re_

        except Exception:
            return None

    def parse_date(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        try:
            time = get_info(web_page, '日期')
            if time is None:
                return None

            return time.split('-')[0], time

        except Exception:
            return None

    def download_photo(self, web_page: str | dict[str, str], photo_path: str, extrafanart_path: str) -> bool:
        try:
            # 照片用的别的网站的，javdb的有水印不得行
            cover_url = f'https://eightcha.com/{jav_number.strip().lower()}/cover.jpg'
            extrafanart_url_list = []

            soup = BeautifulSoup(web_page, 'lxml')
            div = soup.find('div', class_='tile-images preview-images')
            imgs = div.findAll('a', class_='tile-item')
            for img in imgs:
                extrafanart_url_list.append(img['href'])

            # 获取图片数据
            cover_img = self.session.get_image(cover_url)
            extrafanart_img_list = [self.session.get_image(i, headers=headers) for i in extrafanart_url_list]

            # 保存图片
            if cover_img is not None:
                self.image_editor.save(cover_img, f'{photo_path}/poster.jpg')
                self.image_editor.save(cover_img, f'{photo_path}/thumb.jpg')

                # fanart超分放大
                _img = self.image_editor.super_resolution(cover_img)
                self.image_editor.save(_img, f'{photo_path}/fanart.jpg')

            # 保存剧照
            for i, img in enumerate(extrafanart_img_list):
                if img is not None:
                    self.image_editor.save(img, f'{extrafanart_path}/extrafanart-{i + 1}.jpg')


        except Exception:
            return False
