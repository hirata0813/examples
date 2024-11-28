#!/bin/zsh -eu

# 横軸に GPU プログラム開始からの経過時間，縦軸に GPU 稼働率，及び/dev/shm下ファイルへのアクセスタイミングを取り，GPU プログラムを停止した際の GPU 稼働率の時系列変化を折れ線グラフとして描画
# エポック終了，及び停止・再開タイミングを一緒に描画する
# 計算処理と後処理が別れていることを確かめるため，/dev/shm下ファイルへのアクセスタイミングも描画する

# GPU 使用率とタイムスタンプのデータを出力
cat utilization.log | awk '{print NR * 0.1 ", " $1}' > utilization_ts

# syscall.log のfdをファイル名に置換
$PWD/subst-2digit.sh syscall.log

# グラフ縦軸のファイルを引数に取るシステムコールのタイムスタンプを出力
$PWD/calc-filets.sh syscall.log

# エポック終了時のタイムスタンプを出力
$PWD/calc-epochts.sh syscall.log

# SIGSTOP送信時のタイムスタンプを出力
$PWD/calc-sigts.sh syscall.log sigstop.log sigstop_ts

# SIGSTOP送信時のタイムスタンプを出力
$PWD/calc-sigts.sh syscall.log sigcont.log sigcont_ts

# 第一引数：/dev/shm/下ファイルへのアクセス履歴
# 第二引数：GPU稼働率データ
# 第三引数：GPU プログラムの名前(グラフ横軸用)
# 第四引数：SIGSTOPの送信履歴(要素数3のリスト)
# 第五引数：SIGCONTの送信履歴(要素数3のリスト)
# グラフ描画
$PWD/plot-graph.py shmfile_ts utilization_ts "調査対象プログラム1" sigstop_ts sigcont_ts epoch_ts nvidia-uvm_ts