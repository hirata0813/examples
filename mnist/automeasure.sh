#!/bin/bash -eu

# 様々なサイズの行列積を計算し，1ショットの時間を求める

# 前回のログファイルを削除
LOG_FILE="result.txt"

if [ -e ${LOG_FILE} ]; then
  rm ${LOG_FILE}
fi

sizelist=(1000 2500 5000 7500 10000 12500 15000 17500 20000 22500 24000)

for size in "${sizelist[@]}"; do
    $PWD/calc_oneshot_time.sh $size
done
