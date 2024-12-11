#!/bin/bash -eu

# 1ショットの処理時間を求める

# utilization.logの1行目を削除
$PWD/remove_firstline.sh utilization.log

# 1ショットの処理時間を求める
# 第一引数：稼働率のデータファイル
# 第二引数：試行回数(default=10)
# 第三引数：稼働率の閾値(default=0)
# 第四引数：行列のサイズ(N*N)
$PWD/calc_oneshot_time.py $1 $2 $3 $4
