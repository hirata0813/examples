#! /usr/bin/python3
import re
import sys

# 処理時間=(稼働率が閾値を超えている行数 * 0.1 s) / 試行回数

# 第一引数：稼働率のデータファイル
# 第二引数：試行回数(default=10)
# 第三引数：稼働率の閾値(default=0)
# 第四引数：行列のサイズ(N*N)

path = sys.argv[1]
nl = 0 # 稼働率が閾値を超えている行数
trial = int(sys.argv[2]) # 試行回数
threshold = int(sys.argv[3]) # 稼働率の閾値
size = sys.argv[4]

result_path = "result.txt" 

with open(result_path, "+a") as o:
    # テキストファイルの内容を1行ずつ取り出す
    with open(path) as f:
        for line in f:
            # 稼働率を取り出す
            util = int(re.match(r'(\d+)\s+', line)[1])
    
            # 閾値を超えているか判定
            if (util > threshold):
                nl = nl + 1
    
    result = (nl * 0.01) / trial
    print(f"{size}*{size}  {result:.3f} s", file=o)
