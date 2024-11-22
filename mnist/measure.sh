#!/bin/bash -eu

# GPU プログラムをバックグラウンドで実行
strace -ttt -z -o mnist.log python3 main.py &

# nvidia-smi コマンドで GPU プログラムの GPU 使用率を計測
nvidia-smi --query-gpu=utilization.gpu --format=csv -lms 100 -f utilization.log
