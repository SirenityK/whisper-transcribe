from setuptools import setup

# there's a python script called transcribe.py in . which is the main script, add to path
setup(
    name='whisper-transcribe',
    version='1.0',
    install_requires=[
        'faster-whisper',
        'yt-dlp',
    ],
    # add to path
    entry_points= {
        'console_scripts': [
            'transcribe=transcribe:main'
        ]
    }
)
