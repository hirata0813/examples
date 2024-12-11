#! /usr/bin/python3
import argparse
import torch
import subprocess
import sys
import time

# 第一引数：試行回数
# 第二引数：行列のサイズ(N*N)
# 第三引数：ループごとのインターバル

def main():

    print("Start...")
    # Argument settings
    parser = argparse.ArgumentParser(description='PyTorch Matrix matmul')
    parser.add_argument('trial', help='試行回数', type=int)
    parser.add_argument('matrix_size', help='行列のサイズ', type=int)
    parser.add_argument('interval', help='ループごとのインターバル', type=int)
    args = parser.parse_args()

    # デバイスを指定（GPUが利用可能ならGPU、そうでなければCPU）
    device = torch.device("cuda")

    trial = args.trial
    matrix_size = args.matrix_size
    interval = args.interval

    # 100 x 100のランダム行列を作成
    A = torch.randn(matrix_size, matrix_size)  # CPU上で作成
    B = torch.randn(matrix_size, matrix_size)

    # 行列を指定したデバイスに移動
    A = A.to(device)
    B = B.to(device)

    print(f"Calculating matrix multiplication on {device}...")
    
    path = "time.txt"
    with open(path, "+a") as f:
        i = 1
        # 行列の積を計算
        while i <= trial:
            print(f"Loop {i}")
            start = time.time()
            result = torch.matmul(A, B)
            print(f"{result}")
            t = time.time() - start
            print(f"{t}", file=f)
            time.sleep(interval)
            i = i + 1

if __name__ == '__main__':
    main()
