import os

import yt_dlp
from faster_whisper import WhisperModel

from . import config


def seconds_to_minutes(seconds):
    if seconds > 60:
        minute = int(seconds // 60)
        seconds = int(seconds % 60) if seconds % 60 > 9 else f"0{int(seconds % 60)}"
        return f"{minute}:{seconds}m"
    else:
        return f"{int(seconds)}s"


def transcribe(link: str, buffer_path: str, model: str, device="base"):
    with yt_dlp.YoutubeDL(config.ydl_opts) as ydl:
        ydl.download([link])

    videos = os.listdir(buffer_path)
    for video in videos:
        if video.startswith("buffer"):
            bpath = f"{buffer_path}/{video}"
            break

    model = WhisperModel(model, device=device)

    segments, info = model.transcribe(bpath)

    print(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )

    out = []
    tx = []

    for segment in segments:
        start, end = seconds_to_minutes(segment.start), seconds_to_minutes(segment.end)
        text = segment.text[1:]  # [1:] removes the trailing space at the beginning
        message = f"[{start} -> {end}]: {text}\n"
        out.append(message)
        tx.append(text)
        print(message, end="")

    with open("transcript.txt", "w") as f:
        f.seek(0)
        f.truncate(0)
        f.writelines(out)
        f.writelines(
            [
                "\n\nFull transcript:\n",
            ]
        )
        f.write("\n".join(tx))

    os.remove(bpath)
