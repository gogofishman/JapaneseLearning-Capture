class Video:
    def __init__(self):
        self.title = ''
        self.originaltitle = ''
        self.sorttitle = ''
        self.num = ''

        self.mpaa = ''
        self.customrating = ''
        self.rating = ''

        self.director = ''
        self.actor: list[tuple[str, str]] = []
        self.studio = ''
        self.maker = ''

        self.set = ''
        self.tag = []
        self.genre = []
        self.plot = ''

        self.year = ''
        self.premiered = ''
        self.releasedate = ''
        self.release = ''

    def get_actor_list(self, only_female: bool = True) -> list[str]:
        """忽略演员照片，返回只包含演员名字的list"""
        _actor = [a[0] for a in self.actor if only_female and a[2] == 'female']
        return _actor
