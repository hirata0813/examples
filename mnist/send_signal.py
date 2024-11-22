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
    # GPU プログラムはこのプログラムを呼び出すだけで良い
    stop_gpu_process()
    #time.sleep(1) 
    cont_gpu_process()
