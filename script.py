import json
import os
import time
import sys
from queue import Queue

UTILIZATION_THRESH = 10
POWER_THRESH = 0
MEMORY_USED_THRESH = 1024

JOB_QUEUE = Queue()

class Job():
    def __init__(self, work_dir, cmd) -> None:
        self.work_dir = work_dir
        self.cmd = cmd
    
    def execute(self):
        total_cmd = 'cd {} && {}'.format(self.work_dir, self.cmd)
        ret = os.system(total_cmd)
        return ret
        


def get_info():
    return json.load(os.popen('gpustat --json'))['gpus']

def find_free_gpu():
    gpus_info = get_info()
    free_gpu = []
    for info in gpus_info:
        index = info['index']
        utilization = info['utilization.gpu']
        power = info['power.draw']
        memory_used = info['memory.used']
        memory_total = info['memory.total']
    
        if utilization <= UTILIZATION_THRESH and \
            power > POWER_THRESH and \
            memory_used < MEMORY_USED_THRESH:
                gpu_str = f"GPU/id: {index}, GPU/memory: {memory_used}/{memory_total} MiB, GPU/power: {power} W, GPU/utilization: {utilization}\n"
                sys.stdout.write(gpu_str)
                sys.stdout.flush()
                free_gpu.append(index)
    return free_gpu

def narrow_setup(interval=120):
    free_gpu = find_free_gpu()
    while len(free_gpu) == 0:
        # print("no free GPU...")
        time.sleep(interval)
        free_gpu = find_free_gpu()
    job = JOB_QUEUE.get()
    sys.stdout.write("GPU {} is free. Excute cmd:\n work_dir: {}\n cmd: {}\n".format(free_gpu[0], job.work_dir, job.cmd))
    sys.stdout.flush()
    ret = job.execute()
    if ret == 0:
        sys.stdout.write("Execution successed!\n")
        sys.stdout.flush()
    else:
        sys.stdout.write("Execution failed!\n")
        sys.stdout.flush()
        
    
def job_from_input():
    print("Add a new job")
    work_dir = input("Working Directory: ")
    cmd = input("Command: ")
    newjob = Job(work_dir, cmd)
    JOB_QUEUE.put(newjob)

def jobs_from_json(jobs_file):
    with open(jobs_file) as f:
        jobs = json.load(f)['jobs']
    for job in jobs:
        newJob = Job(job['work_dir'], job['cmd'])
        JOB_QUEUE.put(newJob)
    
def main():
    jobs_from_json('jobs.json')
    print("Checking available and free GPU...")    
    
    """
    if there are many jobs in queue, and not block between father and son process
    there may be some wrong when a new job just begin and the utilization of GPU is not too high, 
    which may lead to wrong detection
    """
    # while not JOB_QUEUE.empty():
    #     narrow_setup(10)
    
    narrow_setup(10)


if __name__ == '__main__':
    main()