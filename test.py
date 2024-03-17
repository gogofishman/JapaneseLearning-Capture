# 专门用于测试刮削器的文件

from yolib import Helper

Helper.init(debug=True)


if __name__ == '__main__':
    from api.scraper_run_func import scraper_run
    from api import api
    from queue import Queue

    queue = Queue()
    scraper_run(queue, api, "OVA 初恋時間。 ＃1", "", "test", "Getchu")
