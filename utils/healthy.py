import subprocess
import time
import datetime
import signal
import sys
import os

def check_workload_health(process, is_jobset=False):
    if is_jobset:
        jobset_status = query_jobset_status(process)
        if not jobset_status: 
            return False
    else:
        job_status = query_job_status(process)
        if not job_status: 
            return False

    return True


def query_jobset_status(process):
    stdout = process.stdout.readline().decode().strip()
    if "JobSet: Running" in stdout:
        return True
    elif "JobSet: Failed" in stdout:
        return False
    else:
        return True 


def query_job_status(process):
    stdout = process.stdout.readline().decode().strip()
    if "Job: Succeeded" in stdout:
        return True
    elif "Job: Failed" in stdout:
        return False
    else:
        return True 
def query_jobset_status(process):
    jobset_name = "your-jobset-name"

    try:
        cmd = ["kubectl", "get", "jobset", jobset_name, "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        jobset_data = json.loads(result.stdout)

        all_jobs_completed = True
        cmd_jobs = ["kubectl", "get", "jobs", "--selector=jobset.sigs.k8s.io/jobset-name=" + jobset_name, "-o", "json"]
        result_jobs = subprocess.run(cmd_jobs, capture_output=True, text=True, check=True)
        jobs_data = json.loads(result_jobs.stdout)
        for job in jobs_data.get("items", []):
            if job.get("status").get("succeeded") == None or job.get("status").get("succeeded") < job.get("spec").get("completions"):
                all_jobs_completed = False
                break

        if all_jobs_completed:
            return True
        else:
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl: {e.stderr}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing kubectl output: {e}")
        return False
