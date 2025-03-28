import subprocess
import time
import datetime
import signal
import sys
import os

from utils import *

def poll_workload_status(command, is_jobset):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    failure_intervals = []
    failure_start_time = None
    workload_done = False

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)

    while process.poll() is None:
        time.sleep(1)
        status = check_workload_health(process, is_jobset)

        if not status:
            if failure_start_time is None:
                failure_start_time = datetime.datetime.now()
            print(f"Workload failure detected at: {datetime.datetime.now()}")
        else:
            if failure_start_time:
                failure_intervals.append({'start': failure_start_time, 'end': datetime.datetime.now()})
                failure_start_time = None
            print(f"Workload healthy at: {datetime.datetime.now()}")

    workload_done = True
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Workload exited with error (code {process.returncode}):")
        print(stderr.decode())
        if failure_start_time:
            failure_intervals.append({'start': failure_start_time, 'end': datetime.datetime.now()})
    else:
        print("Workload completed successfully.")
        if failure_start_time:
            failure_intervals.append({'start': failure_start_time, 'end': datetime.datetime.now()})

    output_metrics(failure_intervals)
    return failure_intervals

def signal_handler(sig, frame):
        print(f"\nWorkload interrupted by signal: {signal.Signals(sig).name}")
        if failure_start_time:
            failure_intervals.append({'start': failure_start_time, 'end': datetime.datetime.now()})
        output_metrics(failure_intervals)
        if process.poll() is None:
            process.kill() 
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    if len(sys.argv) < 3:
        print("bad args, please follow: python {workload_script}.py {Is_Jobset (bool)}")
        sys.exit(1)

    workload_command = ["python3", sys.argv[1]]
    failure_data = poll_workload_status(workload_command, sys.argv[2])
    print(f"\nFinal failure data: {failure_data}")