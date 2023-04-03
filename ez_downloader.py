import os
import argparse
from pathlib import Path
from pytube import YouTube


parser = argparse.ArgumentParser(
    prog="ez_downloader", description='Download YouTube videos.')

parser.add_argument('url', type=str, help='YouTube URL')

parser.add_argument('-e', '--extension', type=str,
                    help='File extension', choices=['mp3', 'mp4'], default='mp4')

parser.add_argument('-o', '--outdir', type=str,
                    help='Output directory', default=(Path.home() / "Downloads"))

args = parser.parse_args()

url = args.url
extension = args.extension
outdir = args.outdir


try:
    yt = YouTube(url)
    print(f"Downloading {yt.title}...")

    if extension == "mp3":
        video = yt.streams.filter(abr='160kbps').last()
    elif extension == "mp4":
        video = yt.streams.filter(
            progressive=True, file_extension="mp4").order_by('resolution').desc().first()

    out_file = video.download(output_path=outdir)

    out_file = Path(out_file)
    new_file = out_file.with_suffix(f'.{extension}')
    os.rename(out_file, new_file)

    print(f"Downloaded \"{new_file.absolute()}\"")

except Exception as e:
    print("Something went wrong!")
    print(e)
