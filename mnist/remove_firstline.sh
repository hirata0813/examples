#!/bin/bash -eu

# 第一引数で与えられたファイルの1行目を削除
sed '1d' $1 > tmp.log && mv tmp.log $1
