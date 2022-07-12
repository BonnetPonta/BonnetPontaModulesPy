from datetime import datetime as dt


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


def get_log(msg, datetime: bool = False, default_color: bool = True):
    """ Paramters:
        datetime`bool`: 日時を表示するか否か
        default_color`bool`: カスタム色付きメッセージを使用するか
    """
    res = ""
    if datetime:
        res += f"[{Color.GREEN}{dt.now()}{Color.RESET}] "
    if default_color:
        res += str(Color.CYAN)
    res += f"{msg}{Color.RESET}"
    return res


def log(msg, datetime: bool = False, custom_color: bool = True) -> str:
    """メッセージ文字列をカスタマイズしてprintする"""
    print(get_log(msg, datetime, custom_color))
