#!/bin/zsh -eu

t0=$(head -n 1 $1 | cut -d " " -f 1)
# 各ファイルを引数に持つシステムコールのログを生成

grep /dev/shm/ $PWD/fddata.log | awk -v start="$t0" 'NR==1 {start=start} {printf "%.6f %s\n", $1 - start, $0}' | cut -d ' ' -f 1 > shmfile_ts