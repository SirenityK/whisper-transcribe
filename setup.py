from setuptools import setup

setup(
    name='whisper-transcribe',
    version='1.10',
    license='MIT',
    install_requires=[
        'faster-whisper',
        'pyperclip',
        'yt-dlp'
    ],
    entry_points= {
        'console_scripts': [
            'transcribe=transcribe:main'
        ]
    }
)
