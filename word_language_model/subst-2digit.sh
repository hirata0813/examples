#!/bin/zsh -eu

# 第一引数でstraceのログファイルを取得し，1桁か2桁の数字(fd候補)をファイル名に置き換え
$PWD/subst-2digit.py $1 > fddata.log