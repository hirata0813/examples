#! /usr/bin/python3
import re
import sys

# 処理時間=ログファイルの各行の和の平均
# 第一引数：稼働率のデータファイル
# 第二引数：試行回数(default=10)
# 第三引数：行列のサイズ(N*N)

path = sys.argv[1]
trial = int(sys.argv[2]) # 試行回数
size = sys.argv[3]
sum = 0

result_path = "result.txt" 
with open(result_path, "a") as o:
    # テキストファイルの内容を1行ずつ取り出す
    with open(path) as f:
        for line in f:
            sum = sum + float(line)
    
    result = (sum / float(trial)) * 1000.0
    print(f"{size}*{size}  {result:.3f} ms", file=o)
