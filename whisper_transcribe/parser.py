import argparse
from typing import Literal

import pyperclip

clipboard = pyperclip.paste()


class Types:
    link: str
    model: str
    device: Literal["cuda", "cpu"]


parser = argparse.ArgumentParser(description="Transcribe a video")
parser.add_argument(
    "link", type=str, help="link to the video", default=clipboard, nargs="?"
)
parser.add_argument(
    "-m",
    "--model",
    type=str,
    help="select the model to use",
    default="base",
    choices=["tiny", "base", "medium", "large", "large-v2", "large-v3"],
)
parser.add_argument(
    "-d",
    "--device",
    type=str,
    help="select a device",
    default="cpu",
    choices=["cuda", "cpu"],
)

args: Types = parser.parse_args()
