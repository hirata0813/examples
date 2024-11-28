#! /usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
import sys
import numpy as np
import csv

# 横軸に GPU プログラム開始からの経過時間，縦軸に GPU 稼働率，及び/dev/shm下ファイルへのアクセスタイミングを取り，GPU プログラムを停止した際の GPU 稼働率の時系列変化を折れ線グラフとして描画
# エポック終了，及び停止・再開タイミングを一緒に描画する
# 計算処理と後処理が別れていることを確かめるため，/dev/shm下ファイルへのアクセスタイミングも描画する

# 第一引数：/dev/shm/下ファイルへのアクセス履歴
# 第二引数：GPU稼働率データ
# 第三引数：GPU プログラムの名前(グラフ横軸用)
# 第四引数：SIGSTOPの送信履歴(要素数3のリスト)
# 第五引数：SIGCONTの送信履歴(要素数3のリスト)
# 第六引数：エポック終了のタイミング(要素数3のリスト)

# matplotlibを日本語フォントに対応させる
matplotlib.rc('font', family='Noto Sans CJK JP')

# タイムスタンプ一覧のデータをリストに変換
def create_tslist(file):
    tslist = []
    with open(file, 'r') as f:
        for ts in f:
            tslist.append(float(ts.strip()))
    return tslist


# GPU 使用率のタイムスタンプをリストに変換
def create_util_ts(csv_file):
    tslist = []
    utillist = []
    with open(csv_file, 'r') as f:
        for row in csv.reader(f):
            tslist.append(float(row[0]))
            utillist.append(float(row[1]))
    return tslist, utillist

# グラフの各設定を行う関数
def set_axisopts(axis, axis2, xlabel, ylabel1, ylabel2):
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel1)
    axis2.set_ylabel(ylabel2)
    axis.set_xlim(0,76)
    axis.set_xticks(np.arange(0, 76, step=5))
    axis2.set_ylim(0,100)
    axis2.set_yticks(np.arange(0, 101, step=5))

# グラフに停止・再開・エポック終了のタイミングを描画する関数
def plot_line(ax, ax2, sigstopfile, sigcontfile, epochfile):
    sigstoplist = create_tslist(sigstopfile)

    for i, sigstop in enumerate(sigstoplist):
        if i == 0:
            ax.axvline(sigstop, color='green', linestyle='dashed', linewidth=1, label="停止")
        else:
            ax.axvline(sigstop, color='green', linestyle='dashed', linewidth=1)


    sigcontlist = create_tslist(sigcontfile)
    for i, sigcont in enumerate(sigcontlist):
        if i == 0:
            ax.axvline(sigcont, color='purple', linestyle='dashed', linewidth=1, label="再開")
        else:
            ax.axvline(sigcont, color='purple', linestyle='dashed', linewidth=1)

    epochlist = create_tslist(epochfile)
    for i, epoch in enumerate(epochlist):
        if i == 0:
            ax.axvline(epoch, color='red', linestyle='dashed', linewidth=1, label="エポック終了")
        else:
            ax.axvline(epoch, color='red', linestyle='dashed', linewidth=1)

def main():
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    args = sys.argv

    set_axisopts(ax, ax2, args[3]+"実行開始からの経過時間 (s)", "ファイル", "GPU 稼働率 (%)")

    # /dev/shm下ファイルへのアクセス履歴を描画
    tslist = create_tslist(args[1])
    filelist = ["/dev/shm/*"] * len(tslist)
    ax.scatter(tslist, filelist, s=20, marker=".", color="red")

    # /dev/nvidia-uvmへのアクセス履歴を描画
    tslist = create_tslist(args[7])
    filelist = ["nvidia-uvm"] * len(tslist)
    ax.scatter(tslist, filelist, s=20, marker=".", color="brown")

    # GPU 使用率を折れ線グラフとして描画
    x, y = create_util_ts(args[2])
    ax2.plot(x, y)

    # エポック終了時，シグナル送信時のタイミングで縦線を引く
    plot_line(ax, ax2, args[4], args[5], args[6])

    ax.legend(loc='lower right')

    #fig.savefig('figs/graph2.svg', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()