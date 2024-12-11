#! /usr/bin/python3
import os
import signal
import errno
import subprocess
import time
import sys

# 第一引数：シグナルを送る対象
# 第二引数：SIGSTOPとSIGCONTの間隔
# 第三引数：SIGCONTとSIGKILLの間隔

def stop_gpu_process(target):
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", target], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        current_pid = os.getpid() # 自身のPIDを取得
        pids = [pid for pid in pids if pid and int(pid) != current_pid] # pidsから自身のPIDを除外
        
        if not pids or pids == ['']:
            print("GPU process is not running.")
            return
        
        # 見つかったすべてのプロセスを停止
        for pid in pids:
            print(f"Stopping GPU process with PID: {pid}")
            send_signal(pid, signal.SIGSTOP)
        print("GPU process has been stopped.")

        # SIGSTOP送信時のタイムスタンプを取得
        with open("sigstop.log","a") as f:
            print("{}".format(time.time()), file=f)
    
    except Exception as e:
        print(f"An error occurred: {e}")

def cont_gpu_process(target):
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", target], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        current_pid = os.getpid() # 自身のPIDを取得
        pids = [pid for pid in pids if pid and int(pid) != current_pid] # pidsから自身のPIDを除外
        
        if not pids or pids == ['']:
            print("GPU process is not running.")
            return
        
        # 見つかったすべてのプロセスを再開
        for pid in pids:
            print(f"Continuing GPU process with PID: {pid}")
            send_signal(pid, signal.SIGCONT)
        print("GPU process has been continued.")
    
        # SIGCONT送信時のタイムスタンプを取得
        with open("sigcont.log","a") as f:
            print("{}".format(time.time()), file=f)

    except Exception as e:
        print(f"An error occurred: {e}")

def kill_gpu_process(target):
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", target], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        current_pid = os.getpid() # 自身のPIDを取得
        pids = [pid for pid in pids if pid and int(pid) != current_pid] # pidsから自身のPIDを除外
        
        if not pids or pids == ['']:
            print("GPU process is not running.")
            return
        
        # 見つかったすべてのプロセスを再開
        for pid in pids:
            print(f"Killing GPU process with PID: {pid}")
            send_signal(pid, signal.SIGKILL)
        print("GPU process has been killed.")
    
        # SIGKILL送信時のタイムスタンプを取得
        with open("sigkill.log","a") as f:
            print("{}".format(time.time()), file=f)

    except Exception as e:
        print(f"An error occurred: {e}")

def send_signal(pid, signal):
    try:
        os.kill(int(pid), signal)
    except OSError as e:
        if e.errno != errno.ESRCH: #「No such process」じゃない場合
            raise e

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

def control_gpu_process(target, sleep1, sleep2):
    # ここでGPUプログラムの停止・再開を行う
    stop_gpu_process(target)
    time.sleep(sleep1)
    cont_gpu_process(target)
    time.sleep(sleep2)
    kill_gpu_process(target)
    time.sleep(3)
    stop_nvidia_smi()

def main():
    args = sys.argv
    target = args[1]
    sleep1 = int(args[2])
    sleep2 = int(args[3])
    control_gpu_process(target, sleep1, sleep2)


if __name__ == '__main__':
    # GPU プログラムはこのプログラムを実行するだけで良い
    # 逆にメソッドとして呼び出すと，このプログラムがプロセスとして生成されずうまく停止・再開できない
    main()
