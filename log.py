from datetime import datetime


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


def log(msg):
    """シアン色指定メッセージ"""
    print(f"{Color.CYAN}{msg}{Color.RESET}")


def customLog(msg):
    """色指定なしメッセージ。Colorクラスから選択"""
    print(f"{msg}{Color.RESET}")


def debugLog(msg):
    """日時付きメッセージ"""
    print(f"[{Color.GREEN}{datetime.now()}{Color.RESET}] {Color.CYAN}{msg}{Color.RESET}")
