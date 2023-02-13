import os
import sys
import time

# def gpu_info():
#     gpu_status = os.popen('nvidia-smi | grep %').read().split('|')
#     print(gpu_status)
#     gpu_memory = int(gpu_status[2].split('/')[0].split('M')[0].strip())
#     gpu_power = int(gpu_status[1].split('   ')[-1].split('/')[0].split('W')[0].strip())
#     return gpu_power, gpu_memory

# print(gpu_info())
# s = os.popen('nvidia-smi --query-gpu=utilization.gpu --format=csv').readlines().strip()
# print(s)

def gpu_info(gpu_index):
    query_memory_used = os.popen('nvidia-smi --query-gpu=memory.used --format=csv').readlines()[gpu_index + 1].split()[0]
    gpu_memory_used = int(query_memory_used)
    
    query_memory_utilization = os.popen('nvidia-smi --query-gpu=utilization.memory --format=csv').readlines()[gpu_index + 1].split()[0]
    gpu_memory_utilization = int(query_memory_utilization)
    
    query_power = os.popen('nvidia-smi --query-gpu=power.draw --format=csv').readlines()[gpu_index + 1].split()[0]
    gpu_power = float(query_power)
    
    query_power_utilization = os.popen('nvidia-smi --query-gpu=utilization.gpu --format=csv').readlines()[gpu_index + 1].split()[0]
    gpu_utilization = int(query_power_utilization)
    
    return {"memory_used": gpu_memory_used,
            "memory_utilization": gpu_memory_utilization,
            "power": gpu_power,
            "gpu_utilization": gpu_utilization
            }

# print(gpu_info(0))
import json
a = os.popen('gpustat --json').read()
print(json.loads(a))