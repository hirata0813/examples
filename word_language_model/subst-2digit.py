#! /usr/bin/python3
import re
import sys


# すべてのシステムコールについて，引数を取り出して2桁以内の数字があれば抽出する

# fdlistをハッシュとして用意
fdlist = {'0':'stdin', '1':'stdout', '2':'stderr'}


path = sys.argv[1]
# テキストファイルの内容を1行ずつ取り出す
with open(path) as f:
    for line in f:
        # 行からシステムコール名を取り出す
        res = re.match(r'\d+\.\d+\s+(\w+)', line)
        if res:
            syscall = res.group(1)
            if (syscall == "openat"):
                # システムコール名がopenatなら，第二引数(ファイル名)と返り値(fd)を取り出し，fdlistを更新
                fname = re.search(r'openat\(.*?,\s*"([^"]+)"', line).group(1)
                fd = re.search(r'=\s*(\d+)', line).group(1)
                fdlist[fd] = fname
                print(line, end="")
            else:
                arguments = re.search(r'\((.*)\)', line).group(1)
                # argumentsを,で区切って出力
                arglist = arguments.split(', ')
                flag = 0
                for arg in arglist:
                    #arglistのうち，2桁以内の数字がある場合
                    if (re.match(r'^\d{1,2}$', arg)):
                        flag = 1
                        # fdlist に該当するファイル名があれば置換して出力
                        if (arg in fdlist):
                            print(re.sub(r'\b\d{1,2}\b', fdlist.get(arg), line, 1), end="")
                        # 該当ファイル名がなければ None と出力
                        else:
                            print(re.sub(r'\b\d{1,2}\b', "None", line, 1), end="")
                        # fdは1回しか指定されないはずなので，1回printしたら抜ける
                        break
                if (flag == 0):
                    # 置換が行われなかった場合もその行を出力
                    print(line, end="")