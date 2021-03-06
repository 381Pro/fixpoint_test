#!/usr/bin/env python3
from argparse import ArgumentParser
import re
import datetime
import calendar
import pytz
import sys

# day/month/year:hour:minute:secondをタイムゾーンを反映したタイムスタンプに変換
def time_to_timestamp(time, zone = '+0900'):
    try: # タイムゾーンが地域名だった場合
        time_zone = pytz.timezone(zone)
        dt = datetime.datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        dt = time_zone.localize(dt)
    except pytz.exceptions.UnknownTimeZoneError: # タイムゾーンが[+-]hhmmだった場合
        dt = datetime.datetime.strptime(time + ':' + zone, '%d/%b/%Y:%H:%M:%S:%z')
    return int(dt.timestamp())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-hs", "--host", action="store_true", help="リモートホスト別のアクセス件数を表示")
    parser.add_argument("-t", "--timeframe", action="store_true", help="各時間帯毎のアクセス件数を表示")
    parser.add_argument("-sp", "--split_time", type=int, help="時間帯を何時間区切りに設定するか設定（デフォルトは1）", default=1)
    parser.add_argument("-l", "--log_file", help="解析したいログファイル　複数の場合は空白区切りで指定する（デフォルトは/var/log/httpd/access_log)", default='/var/log/httpd/access_log', nargs='*')
    parser.add_argument("-fs", "--first", help="期間を指定する場合、始まりの時間（day/month/year:hour:minute:secondの書式）", default='01/Jan/0001:00:00:00')
    parser.add_argument("-ls", "--last", help="期間を指定する場合、終わりの時間（day/month/year:hour:minute:secondの書式）", default='31/Dec/9999:23:59:59')
    parser.add_argument("-z", "--zone", help="期間を指定する場合のタイムゾーンを指定する（デフォルトは+0900)", default='+0900')
    args = parser.parse_args()

    HOST = {}
    TIME = {}
    try:
        first_timestamp = time_to_timestamp(args.first, args.zone) # 期間を指定する場合、始まりの時間のタイムスタンプ
        last_timestamp = time_to_timestamp(args.last, args.zone) # 期間を指定する場合、終わりの時間のタイムスタンプ
    except ValueError:
        print("期間指定のフォーマットが正しくありません。正しいフォーマットはday/month/year:hour:minute:second")
        sys.exit(1)

    for log_file in args.log_file:
        with open(log_file, "r", encoding="utf8")as fr:
            line = fr.readline() # 1行ずつファイル読み込み（メモリ節約のため）
            while line:
                log_dict = {}
                log = re.split('["\[\]]', line)
                log_dict["host"], *_ = log[0].split()
                log_dict["time"], log_dict["zone"] = log[1].split()

                """ hostや時間以外も利用したい場合以下を使う
                log_dict["host"], log_dict["identifier"], log_dict["user"] = log[0].split()
                log_dict["time"], log_dict["zone"] = log[1].split()
                log_dict["request"] = log[3]
                log_dict["status"], log_dict["byte"] = log[4].split()
                log_dict["referer"] = log[5]
                log_dict["user-agent"] = log[7]
                """

                time_stamp = time_to_timestamp(log_dict["time"], log_dict["zone"]) # 時間をタイムスタンプに変換
                if(time_stamp < first_timestamp or last_timestamp < time_stamp): # 指定した期間に含まれない場合スキップ
                    line = fr.readline()
                    continue

                if(args.host): # ホスト名をキーとしてアクセス数をカウント
                    try:
                        HOST[log_dict["host"]] += 1
                    except KeyError:
                        HOST[log_dict["host"]] = 1

                if(args.timeframe): #　時間(%h)をキーとしてアクセス数を時間別でカウント
                    try:
                        TIME[log_dict["time"][12:14]] += 1
                    except KeyError:
                        TIME[log_dict["time"][12:14]] = 1

                line = fr.readline() # 次の行を読み込み


    if(args.host):
        HOST = sorted(HOST.items(), key=lambda x:x[1], reverse=True) # アクセスの多いリモートホストの順にソート
        for host, access in HOST:
            print('Host名:', host, ',　アクセス数:', access)

    if(args.timeframe):
        split_time_list = [i for i in range(24)][0::args.split_time] # 時間帯を区切るためのリスト
        split_time_list.append(24) # 24がsplit_timeで割り切れない場合に対応
        for i, j in zip(split_time_list[0:], split_time_list[1:]): # 時間帯ごとのアクセス数の和を求め、表示
            access = 0
            for time1, time2 in TIME.items():
                if(i <= int(time1) and int(time1) <= j-1):
                    access += int(time2)
            print('時間帯: ', str(i).zfill(2) + ':00 ~ ' + str(j-1).zfill(2) + ':59 ,　アクセス数:', access)
