#! /usr/bin/python3
import os
import signal
import errno
import subprocess
import time

def stop_gpu_process():
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", "main.py"], capture_output=True, text=True)
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
    
    except Exception as e:
        print(f"An error occurred: {e}")

def cont_gpu_process():
    try:
        # 実行中のプロセスを検索
        result = subprocess.run(["pgrep", "-f", "main.py"], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        current_pid = os.getpid() # 自身のPIDを取得
        pids = [pid for pid in pids if pid and int(pid) != current_pid] # pidsから自身のPIDを除外
        
        if not pids or pids == ['']:
            print("GPU process is not running.")
            return
        
        # 見つかったすべてのプロセスを停止
        for pid in pids:
            print(f"Continuing GPU process with PID: {pid}")
            send_signal(pid, signal.SIGCONT)
        print("GPU process has been continued.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def send_signal(pid, signal):
    try:
        os.kill(int(pid), signal) 
    except OSError as e:
        if e.errno != errno.ESRCH: #「No such process」じゃない場合
            raise e

def control_gpu_process():
    # ここでGPUプログラムの停止・再開を行う
    stop_gpu_process()
    time.sleep(5)
    cont_gpu_process()

def main():
    control_gpu_process()

if __name__ == '__main__':
    # GPU プログラムはこのプログラムを実行するだけで良い
    # 逆にメソッドとして呼び出すと，このプログラムがプロセスとして生成されずうまく停止・再開できない
    main()
