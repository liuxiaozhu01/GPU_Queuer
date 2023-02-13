import json
import os
import time
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
        os.system(total_cmd)


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
    
        if utilization <= UTILIZATION_THRESH and \
            power > POWER_THRESH and \
            memory_used < MEMORY_USED_THRESH:
                free_gpu.append(index)
    return free_gpu

def narrow_setup(interval=120):
    free_gpu = find_free_gpu()
    while len(free_gpu) == 0:
        time.sleep(interval)
    job = JOB_QUEUE.get()
    print("GPU {} is free. Excute cmd:\n    \
          work_dir: {}\n    \
          cmd: {}".format(free_gpu[0], job.work_dir, job.cmd))
    job.execute()
    
def main():
    print("Add a new job")
    work_dir = input("Working Directory: ")
    cmd = input("Command: ")
    newjob = Job(work_dir, cmd)
    JOB_QUEUE.put(newjob)
    
    narrow_setup(10)


if __name__ == '__main__':
    main()