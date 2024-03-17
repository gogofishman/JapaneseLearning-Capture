from scraper import BaseScraper


class Scraper(BaseScraper):
    def document(self) -> str:
        return '这只是个例子'

    def check_connect(self) -> bool:
        pass

    def search_video_page(self, video_title: str) -> str | dict[str, str] | None:
        pass

    def parse_title(self, web_page: str | dict[str, str]) -> tuple[str, str, str, str] | None:
        pass

    def parse_rating(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        pass

    def parse_director(self, web_page: str | dict[str, str]) -> str | None:
        pass

    def parse_actor(self, web_page: str | dict[str, str]) -> list[tuple[str, str, str]] | None:
        pass

    def parse_studio(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        pass

    def parse_feature(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        pass

    def parse_tag(self, web_page: str | dict[str, str]) -> list[str] | None:
        pass

    def parse_genre(self, web_page: str | dict[str, str], tag: list[str] | None) -> list[str] | None:
        pass

    def parse_date(self, web_page: str | dict[str, str]) -> tuple[str, str] | None:
        pass

    def download_photo(self, web_page: str | dict[str, str], photo_path: str, extrafanart_path: str) -> bool:
        pass
