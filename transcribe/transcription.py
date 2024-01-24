from faster_whisper import WhisperModel
import os
import yt_dlp
import pyperclip
import platform
import argparse

clipboard = pyperclip.paste()
parser = argparse.ArgumentParser(description='Transcribe a video')
parser.add_argument('link', type=str, help='link to the video', default=clipboard, nargs='?')
parser.add_argument('--model', type=str, help='select the model to use', default='base', choices=['tiny', 'base', 'medium', 'large', 'large-v2'])
parser.add_argument('--device', type=bool, help='select a device', default='cuda', choices=['cuda', 'cpu'])
args = parser.parse_args()

device = 'cpu'
try:
    if args.device == 'cpu':
        raise Exception('GPU support is disabled, continuing with CPU')

    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    if not os.getenv('LD_LIBRARY_PATH'):
        raise ModuleNotFoundError('CUDA support is detected, but LD_LIBRARY_PATH is not set, please set it to the path of your CUDA installation. Run the following command before running this script to do it:\n\t' +
            'export LD_LIBRARY_PATH=`python -c \'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))\'`')

    device = 'cuda'
except ModuleNotFoundError as e:
    if args.device == 'cuda':
        print(e)
finally:
    print(f'Using device: {device}')

def map_time(seconds):
        if seconds > 60:
            minute = int(seconds // 60)
            seconds = int(seconds % 60) if seconds % 60 > 9 else f'0{int(seconds % 60)}'
            return f'{minute}:{seconds}m'
        else:
            return f'{int(seconds)}s'

def run():
    if args.link == clipboard:
        print('No link provided, using clipboard')
    try:
        if platform.system() == 'Linux':
            vpath = os.path.join(os.environ['HOME'], 'Videos')
        elif platform.system() == 'Windows':
            vpath = os.path.join(os.environ['USERPROFILE'], 'Videos')
        if not os.path.exists(vpath):
            os.mkdir(vpath)
        os.chdir(vpath)
    except KeyError:
        vpath = os.getcwd()

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'{vpath}/buffer.%(ext)s',
        'forceurl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    if os.path.isfile(args.link):
        vpath = os.path.dirname(args.link)
        bpath = args.link

    else:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.link])

        videos = os.listdir(vpath)
        for video in videos:
            if video.startswith('buffer'):
                bpath = f'{vpath}/{video}'
                break 

    model = WhisperModel(args.model, device=device)

    segments, info = model.transcribe(bpath)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    out = []
    tx = []

    for segment in segments:
        start, end = map_time(segment.start), map_time(segment.end)
        text = segment.text[1:] # [1:] removes the trailing space at the beginning
        message = f'[{start} -> {end}]: {text}\n'
        out.append(message)
        tx.append(text)
        print(message, end='')

    with open('transcript.txt', 'w') as f:
        f.seek(0)
        f.truncate(0)
        f.writelines(out)
        f.writelines([
            '\n\nFull transcript:\n',
        ])
        f.write('\n'.join(tx))

    os.remove(bpath)
