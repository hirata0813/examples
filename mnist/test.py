#! /usr/bin/python3
import argparse
import torch
import subprocess

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
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--no-mps', action='store_true', default=False,
                        help='disables macOS GPU training')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    use_mps = not args.no_mps and torch.backends.mps.is_available()

    torch.manual_seed(args.seed)

    # デバイスを指定（GPUが利用可能ならGPU、そうでなければCPU）
    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")


    # 1000 x 1000のランダム行列を作成
    matrix_size = 1000
    A = torch.randn(matrix_size, matrix_size)  # CPU上で作成
    B = torch.randn(matrix_size, matrix_size)

    # 行列を指定したデバイスに移動
    A = A.to(device)
    B = B.to(device)

    # 行列の積を計算
    print(f"Calculating matrix multiplication on {device}...")
    result = torch.matmul(A, B)

    print("Matrix multiplication completed.")