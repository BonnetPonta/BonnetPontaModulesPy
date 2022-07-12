from datetime import datetime


class Color:
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RESET = '\033[0m'


class Print:
    @staticmethod
    def log(msg):
        print(f"{Color.CYAN}{msg}{Color.RESET}")

    @staticmethod
    def debuglog(msg):
        """日時付き"""
        print(f"[{Color.GREEN}{datetime.now()}{Color.RESET}] {Color.CYAN}{msg}{Color.RESET}")
