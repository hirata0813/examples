#!/bin/bash -eu

# 15000*15000の行列で100回処理を依頼する
# 第一引数：行列のサイズ

# 以前のログファイルを削除

if [ -e sigstop.log ]; then
    rm sigstop.log
fi

if [ -e sigcont.log ]; then
    rm sigcont.log
fi

if [ -e sigkill.log ]; then
    rm sigkill.log
fi

# GPU プログラムをバックグラウンドで実行
strace -ttt -z -o syscall.log ./nonblocking-matmul.py 30 $1 0 &

# nvidia-smi コマンドで GPU プログラムの GPU 使用率を計測
nvidia-smi --query-gpu=utilization.gpu --format=csv -lms 500 -f utilization.log &

# GPU への依頼が完了するのを待つ
sleep 8

# GPU への依頼が完了するタイミングでシグナル送信
echo "Send Signal"
./send_signal.py nonblocking-matmul.py 39 6
