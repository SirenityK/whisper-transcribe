## Troubleshooting

If you're not capable of using cuda, set `LD_LIBRARY_PATH` before running `transcribe`

First install cuBLAS nad cuDNN, strictly install the versions specified as newer ones struggle with shared libraries.

```bash
pip install nvidia-cublas-cu12==12.1.3.1 nvidia-cudnn-cu12==8.9.2.26
```

```bash
export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'`
```
