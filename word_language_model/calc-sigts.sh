#!/bin/zsh -eu

# syscall.logを第一引数，sigstop.log or sigcont.logを第二引数にとり，シグナル送信時のタイムスタンプを出力
# 出力ファイル名は第三引数で指定

t0=$(head -n 1 $1 | cut -d " " -f 1)
cat $2 | awk -v start="$t0" 'NR==1 {start=start} {printf "%.6f %s\n", $1 - start, $0}' | cut -d ' ' -f 1 | awk '{print $0}' > $3