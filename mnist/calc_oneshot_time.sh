#!/bin/zsh -eu

### 行列積を計算し，1ショットの処理時間を求める
###  第一引数：行列のサイズ

# 前回のログファイルを削除
LOG_FILE="time.txt"

if [ -e ${LOG_FILE} ]; then
  rm ${LOG_FILE}
fi

# GPU プログラムを開始
# 第一引数：試行回数
# 第二引数：行列のサイズ(N*N)
# 第三引数：ループごとのインターバル
./matmul.py 10 $1 3 

# ログファイルの1行目を削除
#./remove_firstline.sh time.txt
# ログファイルから1ショットの時間を計算
# 第一引数：稼働率のデータファイル
# 第二引数：試行回数(default=10)
# 第三引数：行列のサイズ(N*N)
./calc_oneshot_time.py time.txt 10 $1

