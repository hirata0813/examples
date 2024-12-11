#!/bin/bash -eu

# 行列積を計算し，1ショットの処理時間を求める
# 第一引数：行列のサイズ

# 以前のログファイルを削除
echo "" > sigcont.log
echo "" > sigstop.log
echo "" > sigkill.log

# GPU プログラムをバックグラウンドで実行
./matmul.py 10 $1 3 &

# nvidia-smi コマンドで GPU プログラムの GPU 使用率を計測
nvidia-smi --query-gpu=utilization.gpu --format=csv -lms 10 -f utilization.log

# 1ショットの処理時間を求める
./calc_oneshot_time.sh $PWD/utilization.log 10 0 $1
