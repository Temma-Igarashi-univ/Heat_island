# 関東地方のUHIIと汚染物質のデータ解析

これは、東京大学において1年次に実施される、英語での論文執筆を学ぶ授業 ALESS (Active Learning of English for Science Students)の一環で制作されたプログラムです。  
[気象庁の気温データ](https://www.data.jma.go.jp/stats/etrn/index.php?prec_no=&block_no=&year=&month=&day=&view=)、
および国立環境研究所の「[環境展望台 大気汚染常時監視データ](https://tenbou.nies.go.jp/download/)」
「[大気環境測定局データ](https://www.nies.go.jp/igreen/tm_down.html)」を使用します。(閲覧は2024年6月2日)

ここに掲載しているコードは閲覧用であり、再使用は想定されていませんが、ご利用になる場合は次の手順で操作を行なってください。
1. Python, 必要なパッケージ (各ファイルの頭に記載) およびGoogle Chromeを入手する。
2. asys.pyに記載の通り、国立環境研究所のデータをダウンロードし処理する。
3. temptest.py 24行目のメールアドレスを自分のものに書き換える。
4. asys.py, calc_epd.py, correlation.pyの順に実行する。
尚、calc.epd.py実行時点で解析に必要なファイルは全て揃うので、correlation.pyと異なるファイルで異なる解析手法を試みることも可能です。

ファイルの内容は次のとおりです。  
asys.py: データ収集およびUHIIを計算するファイル。  
calc_epd.py: 汚染物質データを補間して気温観測所に対応する場所における濃度を算出するファイル。  
constants.py: データ保持クラスを定義するファイル。  
coord.json: 実験に使用した地点のデータを上記の気象庁のデータページより収集し使用可能な形に書き直したファイル。  
correlation.py: 相関係数計算及びグラフプロットを行うためのファイル。  
readme-en.md: readme.mdの英訳。  
readme.md: リポジトリ説明ファイル。  
temptest.py: 気象庁サイトより平均気温をスクレイピングするためのファイル。

Python 3.12.2 および MacBook Pro (M3チップ搭載, 12コアCPU, 36GBメモリ) での動作を確認しています。  
Google Chrome のバージョンは 125.0.6422.141 (Official Build) (arm64) です。

その他直接利用したライブラリは以下のとおりです。  
beautifulsoup4 (https://pypi.org/project/beautifulsoup4/) v4.12.3  
chromedriver-binary (https://github.com/danielkaiser/python-chromedriver-binary) v125.0.6422.78.0  
dill (https://github.com/uqfoundation/dill) v0.3.8  
geographiclib (https://geographiclib.sourceforge.io/Python/2.0) v2.0  
matplotlib (https://pypi.org/project/matplotlib/) v3.9.0  
numpy (https://numpy.org) v1.26.4  
selenium (https://www.selenium.dev) v4.21.0