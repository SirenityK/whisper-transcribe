from . import config, transcription


def main():
    from .parser import args

    print("Using device:", args.device)
    transcription.transcribe(args.link, config.vpath, args.model, args.device)
