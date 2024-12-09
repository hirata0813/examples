#!/bin/bash -eu

# 以前のログファイルを削除
echo "" > sigcont.log
echo "" > sigstop.log
# GPU プログラムをバックグラウンドで実行
strace -ttt -z -o syscall.log python3 test1.py &

# nvidia-smi コマンドで GPU プログラムの GPU 使用率を計測
nvidia-smi --query-gpu=utilization.gpu --format=csv -lms 100 -f utilization.log
