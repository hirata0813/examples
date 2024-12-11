#!/bin/bash -eu

# 様々なサイズの行列積を計算し，1ショットの時間を求める
# 第一引数：行列のサイズ

# 前回のログの中身を空にする
echo "" > result.txt

sizelist=(1000 2500 5000 7500 10000 12500 15000 17500 20000 22500)

for size in "${sizelist[@]}"; do
    $PWD/measure.sh $size
done
