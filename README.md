# fixpoint_test
プログラミング試験（フィックスポイント）\
$ python3 fix.py --host --time \
または \
$ fix.py --host --time \
で実行できます。 \
細かいオプションは-hを追加すると表示されます。 \
$ fix.py -h \
usage: fix.py [-h] [-hs] [-t] [-l [LOG_FILE [LOG_FILE ...]]] [-fs FIRST] \
              [-ls LAST] [-z ZONE] \

optional arguments: \
  -h, --help            show this help message and exit \
  -hs, --host           リモートホスト別のアクセス件数を表示 \
  -t, --timeframe       各時間帯毎のアクセス件数を表示 \
  -l [LOG_FILE [LOG_FILE ...]], --log_file [LOG_FILE [LOG_FILE ...]] 解析したいログファイル（デフォルトは/var/log/httpd/access_log) \
  -fs FIRST, --first FIRST 期間を指定する場合、始まりの時間（day/month/year:hour:minute:secondの書式） \
  -ls LAST, --last LAST 期間を指定する場合、終わりの時間（day/month/year:hour:minute:secondの書式） \
  -z ZONE, --zone ZONE  期間を指定する場合のタイムゾーンを指定する（デフォルトは+0900) 
