# GPU_Queuer
Make the GPU running all the time. GPU 排队

- Self-used script, untested. There is room for improvement, more on that later
自用脚本，未经测试。有待改进，以后再说

## Running 

This script is based on **gpustat** command. So it should be installed firstly
```
pip install gpustat
```

Then run the scripy in backend.
```shell
nohup python script.py JSON_FILE >check.log 2>&1 &
```
JSON_FILE contains the **work directory** and the **command** to run you GPU-Occupation program