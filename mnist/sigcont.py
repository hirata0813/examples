#! /usr/bin/python3
import os
import signal
import errno
import subprocess

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
            print(f"Stopping GPU process with PID: {pid}")
            send_signal(pid, signal.SIGCONT)
        print("GPU process has been stopped.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def send_signal(pid, signal):
    try:
        os.kill(int(pid), signal) 
    except OSError as e:
        if e.errno != errno.ESRCH: #「No such process」じゃない場合
            raise e

def main():
    cont_gpu_process()

if __name__ == '__main__':
    main()