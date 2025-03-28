import subprocess
import time
import json  # If you're parsing JSON output

def check_workload_health(process, is_jobset=False):
    """
    Determines workload health by polling its status.

    Args:
        process: The subprocess.Popen object representing the running workload.
        is_jobset: True if the workload is a JobSet, False if it's a Job.

    Returns:
        True if the workload is healthy, False otherwise.
    """

    stdout = process.stdout.readline().decode().strip()
    stderr = process.stderr.readline().decode().strip()

    if "ERROR" in stdout or "Exception" in stderr:
        return False

    if is_jobset:
        # Query JobSet status (replace with your actual JobSet status check)
        jobset_status = query_jobset_status(process)
        if not jobset_status:  # Or however you define JobSet failure
            return False
    else:
        # Query Job status (replace with your actual Job status check)
        job_status = query_job_status(process)
        if not job_status:  # Or however you define Job failure
            return False

    return True


def query_jobset_status(process):
    """
    Replace this with your actual logic to query the JobSet status.

    This is a placeholder and should be implemented based on your system.
    For example, you might:
    - Parse output from the process's stdout/stderr.
    - Call an API to check the JobSet's status.
    - Check for specific files or states.

    Args:
        process: The subprocess.Popen object.

    Returns:
        True if the JobSet is healthy, False otherwise.
    """
    # Example (replace with your actual logic):
    # This is a very basic example; you'll need to adapt it.
    stdout = process.stdout.readline().decode().strip()
    if "JobSet: Running" in stdout:
        return True
    elif "JobSet: Failed" in stdout:
        return False
    else:
        return True  # Or perhaps raise an exception if you can't determine


def query_job_status(process):
    """
    Replace this with your actual logic to query the Job status.

    This is a placeholder and should be implemented based on your system.
    For example, you might:
    - Parse output from the process's stdout/stderr.
    - Call an API to check the Job's status.
    - Check for specific files or states.

    Args:
        process: The subprocess.Popen object.

    Returns:
        True if the Job is healthy, False otherwise.
    """
    # Example (replace with your actual logic):
    # This is a very basic example; you'll need to adapt it.
    stdout = process.stdout.readline().decode().strip()
    if "Job: Succeeded" in stdout:
        return True
    elif "Job: Failed" in stdout:
        return False
    else:
        return True  # Or perhaps raise an exception if you can't determine