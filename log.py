from datetime import datetime, timedelta


class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'


def jst():
    return datetime.utcnow() + timedelta(hours=9)


def log_string(msg, datetime: bool = False, color: Color = Color.CYAN) -> str:
    """ Parameters:
    --------------
        datetime`bool`: 日時を表示するか否か
        color`bool`: print色
    """
    res = f"{color}{msg}{Color.RESET}"
    if datetime:
        res = f"[{Color.GREEN}{jst()}{Color.RESET}] " + res
    return res


def log_print(msg, datetime: bool = False, color: Color = Color.CYAN) -> str:
    """メッセージ文字列をカスタマイズしてprintする"""
    print(log_string(msg, datetime, color))
