#! /usr/bin/python3
import argparse
import torch
import subprocess
import sys
import time

# 第一引数：試行回数
# 第二引数：行列のサイズ(N*N)
# 第三引数：ループごとのインターバル

def stop_nvidia_smi():
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", "nvidia-smi"], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        
        if not pids or pids == ['']:
            print("nvidia-smi is not running.")
            return
        
        # 見つかったすべてのプロセスを停止
        for pid in pids:
            print(f"Stopping nvidia-smi process with PID: {pid}")
            subprocess.run(["kill", "-TERM", pid])
        print("nvidia-smi has been stopped.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def main():

    print("Start...")
    # Argument settings
    parser = argparse.ArgumentParser(description='PyTorch Matrix matmul')
    parser.add_argument('trial', help='試行回数', type=int)
    parser.add_argument('matrix_size', help='行列のサイズ', type=int)
    parser.add_argument('interval', help='ループごとのインターバル', type=int)

    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--no-mps', action='store_true', default=False,
                        help='disables macOS GPU training')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    use_mps = not args.no_mps and torch.backends.mps.is_available()

    # デバイスを指定（GPUが利用可能ならGPU、そうでなければCPU）
    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

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
    
    i = 1
    # 行列の積を計算
    while i <= trial:
        print(f"Loop {i}")
        result = torch.matmul(A, B)
        print(f"Finished: {result}")
        i = i + 1
        time.sleep(interval)


if __name__ == '__main__':
    main()
    # nvidia-smi を停止
    stop_nvidia_smi()
