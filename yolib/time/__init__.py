from datetime import datetime


class TimeHelper:

    @staticmethod
    def timestamp() -> float:
        """获取当前时间戳 (秒级)"""
        return datetime.now().timestamp()

    @staticmethod
    def timestamp_ms() -> int:
        """获取当前时间戳 (毫秒级)"""
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def now_format() -> str:
        """返回格式化后的当前时间，精确到毫秒，如（'2024-03-04 18:25:09.346'）"""
        time = datetime.now()
        microsecond = str(round(time.microsecond / 1000000, 3))[2:]

        zero_count = 3 - len(microsecond)
        microsecond = microsecond + "0" * zero_count

        return f"{time.strftime('%Y-%m-%d %H:%M:%S')}.{microsecond}"
