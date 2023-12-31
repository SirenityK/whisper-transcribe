from faster_whisper import WhisperModel
import os
import yt_dlp
import argparse

parser = argparse.ArgumentParser(description='Transcribe a video')
parser.add_argument('link', type=str, help='link to the video')
# allow tab completion for model names  
parser.add_argument('--model', type=str, help='select the model to use', default='medium', choices=['tiny', 'base', 'medium', 'large', 'large-v2'])

parser.add_argument('--use-gpu', type=bool, help='use gpu if available', default=True)
args = parser.parse_args()

try:
    if not args.use_gpu:
        raise Exception('GPU support is disabled, continuing with CPU')
    
    import nvidia.cublas.lib
    import nvidia.cudnn.lib
    device = 'cuda'
except ModuleNotFoundError as e:
    if args.use_gpu:
        print('GPU support not found, continuing with CPU')
        print(e)
    device = 'cpu'

def map_time(seconds):
        if seconds > 60:
            minute = int(seconds // 60)
            seconds = int(seconds % 60) if seconds % 60 > 9 else f'0{int(seconds % 60)}'
            return f'{minute}:{seconds}m'
        else:
            return f'{int(seconds)}s'

def run():
    try:
        vpath = '/home/' + os.environ['USER'] + '/Videos'
        os.chdir(vpath)
    except KeyError:
        vpath = os.getcwd()


    # os.system(f'yt-dlp -x {args.link} -o \'{vpath}/buffer.%(ext)s\'')
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'{vpath}/buffer.%(ext)s',
        'forceurl': True,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    #check first if args.link is the path to a local file
    if os.path.isfile(args.link):
        vpath = os.path.dirname(args.link)
        bpath = args.link

    else:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([args.link])

        videos = os.listdir(vpath)
        for video in videos:
            if video.startswith('buffer'):
                bpath = f'{vpath}/{video}'
                break 

    # Use the model to transcribe the video, use GPU if available
    model = WhisperModel(args.model, device=device)

    segments, info = model.transcribe(bpath)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    out = []
    tx = []

    for segment in segments:
        start, end = map_time(segment.start), map_time(segment.end)
        text = segment.text
        out.append(f'[{start} -> {end}]: {text}')
        tx.append(text)
        print(f'[{start} -> {end}]: {text}')

    with open('transcript.txt', 'w') as f:
        f.write('\n'.join(out))
        f.write('\n\n')
        f.write('\n'.join(tx))

    os.remove(bpath)
