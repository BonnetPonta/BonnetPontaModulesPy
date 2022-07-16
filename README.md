# BonnetPontaModulesPy
## なにこれ？
自分用のpython module  
`git clone`で`lib`ディレクトリにクローンし、`import`して使える。  
順次追加していく予定。  

## どうやって使うの？
使用例
```
# ディレクトリ構造
- lib
    └ (git clone した この)BonnetPontaModulesPy
- src
    └ app.py
```
の場合、app.pyからlib/BonnetPontaModulesPyを呼び出すには、  
下記の記述が必要になる。  
```py
# 呼び出し先 src/app.py
import os
import sys

sys.path.append(os.getcwd())
# これで lib から記述できるようになる
from lib.BonnetPontaModulesPy.log import Color, log_print, log_string
```
を呼び出し先ファイルに追記し、`import`してご使用ください。  
`sys.path.append(os.getcwd())`をすることで、上位ディレクトリの`lib`から`import`できるようにしています。

# 各file説明
## `log.py`
logを出したいときに時に役立つmoduleたち。  
色付き文字列、print時に色付けたいとき、日時を表示させたいとき  

## `scrapes.py`
スクレイピングに役立つmodulesたち。  
requests, BeautifulSoup, aiohttp, seleniumに対応  

## `twitter.py`
twitter APIであるtweepyを使ってTL,user tweetを取得・投稿する。  