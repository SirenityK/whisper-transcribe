import importlib.util
import os
import platform

from .parser import args

if all(
    (
        importlib.util.find_spec("nvidia.cublas.lib"),
        importlib.util.find_spec("nvidia.cudnn.lib"),
        not os.getenv("LD_LIBRARY_PATH"),
        args.device == "cuda",
    )
):
    raise ModuleNotFoundError(
        "CUDA support is detected, but LD_LIBRARY_PATH is not set, please set it to the path of your CUDA installation. Run the following command before running this script to do it:\n\t"
        + "export LD_LIBRARY_PATH=`python -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + \":\" + os.path.dirname(nvidia.cudnn.lib.__file__))'`"
    )

vpath = os.getcwd()

if platform.system() == "Linux":
    vpath = os.path.join(os.environ["HOME"], "Videos")
elif platform.system() == "Windows":
    vpath = os.path.join(os.environ["USERPROFILE"], "Videos")
if not os.path.exists(vpath):
    os.mkdir(vpath)

ydl_opts = {
    "format": "m4a/bestaudio/best",
    "outtmpl": f"{vpath}/buffer.%(ext)s",
    "forceurl": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
}
