#!/bin/zsh -eu

t0=$(head -n 1 $1 | cut -d " " -f 1)
grep "エポックが終了しました" $1 | awk -v start="$t0" 'NR==1 {start=start} {printf "%.6f %s\n", $1 - start, $0}' | cut -d ' ' -f 1 | awk '{print $0}' > epoch_ts