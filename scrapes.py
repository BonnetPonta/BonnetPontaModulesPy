import asyncio
import random
import time
from http.client import HTTPException
from traceback import format_exc
from types import NoneType

import aiohttp
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"


def wait_sleep(sleepTime=None):
    """sleepする時間: 指定なしなら 3~5s待機
        >>> # normal
            time.sleep(sleepTime)
        >>> # async
            await asyncio.sleep(sleepTime)"""
    if sleepTime is None:
        sleepTime = random.randint(3, 5)
    time.sleep(sleepTime)


def get_html(load_url: str, cookies=None):
    """ 引数URLからhtml情報を返す。かつ、html.urlで正式なURLかも確認する
    update_SQLComicURL `bool`: 主にComic URLの時にTrue"""
    def get_request(load_url: str, cookies=None, headers_lang_ja=False):
        """ HTTP requests.最高3回再起処理を行い、HTML,Noneの何れかを返す

        .. Note タイムアウトを設定しないと数分スタックする

        Args:
            load_url `str`: URL
            cookies `dict[str]` | `None`: cokkies.
            headers_lang_ja `bool`: response HTML is Japanese.
            timeout `int` or `float`

        Returns:
            html `class` | `None`: html
        """
        headers = {'User-Agent': USER_AGENT}
        if headers_lang_ja:
            headers["Accept-Language"] = "ja"

        for i in range(3):
            if 0 < i:
                wait_sleep(6)
            else:  # 1回目はランダム秒
                wait_sleep()
            print(
                f"URL: {load_url}\ncookies: {cookies}\nheaders: {headers}")
            try:
                if cookies is None:
                    html = requests.get(load_url, timeout=(3.05, 9.05),
                                        headers=headers)
                else:
                    html = requests.get(load_url, timeout=(3.05, 9.05),
                                        cookies=cookies, headers=headers)
                # 日本語文字化け対策
                html.encoding = html.apparent_encoding
            except requests.Timeout:
                print(
                    f"{i+1}/3回目の HTTP request Timeout error.URL is {load_url}")
            else:
                print(f"success {i+1}/3回目の HTTP request.URL is {load_url}")
                return html

    if not load_url.startswith("https"):
        print(f"{load_url} はhttps通信ではありません。")
    html = get_request(load_url, cookies)
    if html is None:  # Timeout 以後htmlでNoneTypeエラー回避 -> 終了
        print(f"URL: {load_url} は、Noneを返す無効なURLです。")
        return
    elif html.status_code != 200:
        base_url = str(load_url.split(".com")[0]) + ".com"
        print(
            f"1/2 回目: {load_url} でステータスコード {html.status_code} が返されました。\nパラメーターを削除した {base_url} で再度status codeを確認します。")
        html = get_request(base_url, cookies)
        if html is None:  # 以後htmlでNoneTypeエラー回避 -> 終了
            return
        elif html.status_code != 200:  # 素のURLでもHTTP Errorならエラー表示して終了
            print(
                f"2/2 回目: {load_url} でステータスコード {html.status_code} が返されました。\nHeader情報: {html.headers}")
            return
    return html


def get_soup(load_url: str, cookies=None):
    """Beutifulsoupでhtmlを解析した値を返す。
    .. 基本はtextで、文字化けする時(主に古いサイト)はcontentを指定。

    Parameters
    -----------
    load_url:`str`
        URL名を指定
    cookies:`dict[str]`
        cookies

    Returns
    --------
    soup:`beautifulsoup`
        htmlを返す
    error:`exc`
        - status codeが 200でない
        - parser typeが <text|content> でない
    """
    html = get_html(load_url, cookies)
    if html is None:  # 以後htmlでNoneTypeエラー回避 -> 終了
        return
    elif html.status_code == 200:
        return BeautifulSoup(html.text, "html.parser")
    else:
        print(f"URL: {load_url} は、status code: {html.status_code} が返されたため終了します。")


async def get_aiohttp(load_urls: list[str]) -> dict[str, str]:
    """並列処理でtask化し、高速requestする
    Arg:
        load_urls: `list[str]`
    Returns:
        url,redirect_url,status_code,html,soup: `dict`"""
    async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}) as session:
        async def _fetch_and_scrape(load_url: str):
            data = {"url": load_url}
            if not load_url.startswith("https"):
                print(f"{load_url} はhttps通信ではありません。")
            try:
                async with session.get(load_url, timeout=9) as html:
                    if html is None:
                        raise NoneType(
                            f"URL: {load_url} は、Noneを返す無効なURLです。\nまたは、URLが更新された可能性があります。")
                    elif html.status != 200:
                        raise HTTPException(
                            f"{load_url} で、status code: {html.status} が返されました。\nheaders: {html.headers}")
                    data.update({
                        "redirect_url": str(html.url),
                        "status_code": html.status,
                        "html": await html.text(),
                        "soup": BeautifulSoup(await html.text(), "html.parser")
                    })
            except Exception as e:
                print(e, format_exc(), f"_fetch_and_scrape関数 {load_url} で例外が発生しました。")
            finally:
                return data
        return await asyncio.gather(*[_fetch_and_scrape(load_url) for load_url in load_urls], return_exceptions=True)


def get_soup_selenium(load_url):
    """seleniumでsoupを取得した値を返す。
    ..  cssとか取得したいときにseleniumを使用
    """
    options = ChromeOptions()
    # https://boardtechlog.com/2020/08/programming/seleniumchromeでよく使うchromeoptionsまとめ/
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)
        driver.get(load_url)
        html = driver.page_source.encode('utf-8')
        if html is None:
            print(
                f"selenium htmlがNoneを返されたため、カットします。\nurl: {load_url}")
        else:
            return BeautifulSoup(html, "html.parser")
        driver.quit()
    except Exception as e:
        print(e, format_exc(), f"selenium driver. url: {load_url}")
        print(f"ヒント1:恐らくherokuにbuild2つを追加していないため、selenium driverを使用できません。\nchromedrive: https://github.com/heroku/heroku-buildpack-chromedriver.git と\ngoogle-chrome: https://github.com/heroku/heroku-buildpack-google-chrome.git\nの2つを追加してください。\nヒント2:また、herokuにインストールするため、ローカル環境ではエラーになります。")
    finally:
        try:
            driver.quit()
        except:
            pass
