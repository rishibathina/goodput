import subprocess
import time
import datetime
import signal
import sys
import os

def output_metrics(failure_intervals):
    if not failure_intervals:
        print("\nNo failures detected.")
        return

    print("\nFailure Metrics:")
    total_downtime = datetime.timedelta()
    for interval in failure_intervals:
        start_str = interval['start'].strftime("%Y-%m-%d %H:%M:%S")
        end_str = interval['end'].strftime("%Y-%m-%d %H:%M:%S")
        duration = interval['end'] - interval['start']
        total_downtime += duration
        print(f"- Start: {start_str}, End: {end_str}, Duration: {duration}")

    print(f"\nTotal Downtime: {total_downtime}")