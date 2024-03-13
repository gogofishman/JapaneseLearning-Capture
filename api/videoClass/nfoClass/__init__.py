import xml.etree.ElementTree as ET

from api.videoClass import Video


def xml_format(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_format(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class Nfo:
    def __init__(self, video: Video, path: str):
        self.video = video
        self.file_path = path

        # xml
        self.xml = ET.Element('movie')

        self.add_element('title', video.title)
        self.add_element('originaltitle', video.originaltitle)
        self.add_element('sorttitle', video.sorttitle)
        self.add_element('num', video.num)

        self.add_element('mpaa', video.mpaa)
        self.add_element('customrating', video.customrating)
        self.add_element('rating', video.rating)

        self.add_element('director', video.director)
        for a in video.actor:
            actor = self.add_element('actor')
            self.add_element('name', a[0], actor)
            self.add_element('thumb', a[1], actor)
            self.add_element('gender', a[2], actor)
        self.add_element('studio', video.studio)
        self.add_element('maker', video.maker)

        self.add_element('set', video.set)
        for t in video.tag:
            self.add_element('tag', t)
        for g in video.genre:
            self.add_element('genre', g)
        self.add_element('plot', video.plot)

        self.add_element('year', video.year)
        self.add_element('premiered', video.premiered)
        self.add_element('releasedate', video.releasedate)
        self.add_element('release', video.release)

        self.add_element('poster', 'poster.jpg')
        self.add_element('fanart', 'fanart.jpg')
        self.add_element('fanart', 'thumb.jpg')

        self.add_element('scraper', video.scraper)

        xml_format(self.xml)

    def save(self):
        tree = ET.ElementTree(self.xml)
        tree.write(self.file_path, encoding='utf-8', method="xml")

    def add_element(self, key: str, value: str = '', parent: ET.Element = None):
        """
        添加元素
        :param value:
        :param key:
        :param parent:默认为None，表示根元素
        :return: 返回当前创建的元素对象
        """

        parent = self.xml if parent is None else parent
        element = ET.SubElement(parent, key)
        if value != '':
            element.text = value
        return element
