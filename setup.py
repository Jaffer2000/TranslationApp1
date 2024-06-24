from setuptools import setup, find_packages

setup(
    name="speech_translator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "speechrecognition",
        "requests",
        "pyaudio",
    ],
    entry_points={
        'console_scripts': [
            'speech-translator=speech_translator.main:main',
        ],
    },
)
