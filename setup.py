from setuptools import setup, find_packages

setup(
    name='Music-Recognizer-Namer-Saver',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'shazamio==0.5.1',
        'tqdm==4.66.2',
        'PyQt5==5.15.10',
    ],
    python_requires='>=3.12',
    author='CLEMENT Pierre',
    author_email='pierraored@gmail.com',
    description='Use Shazam to find the musics title and author to copy files with the name in a folder.',
)
