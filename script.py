import json
import os
import time

UTILIZATION_THRESH = 10
POWER_THRESH = 0
MEMORY_USED_THRESH = 1024

CMD_QUEUE = ""

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
    print("GPU {} is free. Excute cmd: {}".format(free_gpu[0], CMD_QUEUE[0]))
    os.system(CMD_QUEUE[0])


if __name___ == '__main__':
    narrow_setup(2)