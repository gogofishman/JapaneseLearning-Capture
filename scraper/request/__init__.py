import time
from requests import Session, Response, RequestException

from yolib import Helper


class MySession(Session):
    """重写的Session类

    自动配置了get、post方法的代理、超时、重连次数、连接间隔等网络连接设置
    """

    next_connect_time = 0
    connect_sleep = 3
    connect_reconnections = 3

    def get(self, url, **kwargs) -> Response | None:
        r"""发送一个GET请求。返回 :class:`Response` 对象。

        :param url: 新的 :class:`Request` 对象的URL。
        :param kwargs: ``request`` 接受的可选参数。
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", True)

        # 设置每次连接之间不小于 connect_sleep
        if time.time() < self.next_connect_time:
            time.sleep(self.next_connect_time - time.time())
            self.next_connect_time = time.time() + self.connect_sleep
        if self.next_connect_time == 0:
            self.next_connect_time = time.time() + self.connect_sleep

        # 如果连接失败尝试connect_reconnections次重连
        for i in range(self.connect_reconnections):
            try:
                response = self.request("GET", url, **kwargs)
                response.raise_for_status()  # 检查响应状态码，如果不是 2xx，则抛出异常
                return response
            except RequestException as e:
                Helper.logging.debug(f"连接失败，正在进行第 {i + 1} 次重连... [{url}]")
                time.sleep(1)
        Helper.logging.debug(f"连接失败，已达到最大重试次数。 [{url}]")
        return None

    def post(self, url, data=None, json=None, **kwargs) -> Response | None:
        r"""发送一个POST请求。返回 :class:`Response` 对象。

        :param url: 新的 :class:`Request` 对象的URL。
        :param data: (可选) 要发送到 :class:`Request` 的请求体的字典、元组列表、字节或类文件对象。
        :param json: (可选) 要发送到 :class:`Request` 的请求体中的 JSON 数据。
        :param \*\*kwargs: ``request`` 接受的可选参数。
        :rtype: requests.Response
        """

        # 设置每次连接之间不小于 connect_sleep
        if time.time() < self.next_connect_time:
            time.sleep(self.next_connect_time - time.time())
            self.next_connect_time = time.time() + self.connect_sleep

        # 如果连接失败尝试connect_reconnections次重连
        for i in range(self.connect_reconnections + 1):
            try:
                response = self.request("POST", url, data=data, json=json, **kwargs)
                response.raise_for_status()  # 检查响应状态码，如果不是 2xx，则抛出异常
                return response
            except RequestException as e:
                Helper.logging.debug(f"连接失败，正在进行第 {i + 1} 次重连... [{url}]")
                time.sleep(1)
        Helper.logging.debug(f"连接失败，已达到最大重试次数。 [{url}]")
        return None

    def get_image(self, url: str, headers: dict[str, str] = None, cookies: dict[str, str] = None) -> bytes | None:
        """获取静态图片，不考虑连接的间隔时间"""

        # 如果连接失败尝试connect_reconnections次重连
        for i in range(self.connect_reconnections):
            try:
                response = self.request("GET", url, headers=headers, cookies=cookies)
                response.raise_for_status()  # 检查响应状态码，如果不是 2xx，则抛出异常
                return response.content
            except RequestException as e:
                Helper.logging.debug(f"连接失败，正在进行第 {i + 1} 次重连... [{url}]")
                time.sleep(1)
        Helper.logging.debug(f"连接失败，已达到最大重试次数。 [{url}]")
        return None


session = MySession()
