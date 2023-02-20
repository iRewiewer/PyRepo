import argparse
import re
from os import path, environ, mkdir, system
from pathlib import Path
from pytube import Playlist, YouTube
from time import sleep

def Init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-isplaylist', type=str, required=True)
    parser.add_argument('-downloadpath', type=str, required=True)
    parser.add_argument('-videoformat', type=str, required=True)
    parser.add_argument('-links', type=str, required=True)
    args = parser.parse_args()

    isPlaylist = True if args.isplaylist.lower() == "true" else False
    videoFormat = "mp4" if args.videoformat.lower() == "mp4" else "mp3"
    links = args.links.split(' ')

    print("[Downloading playlist(s)]") if isPlaylist == True else print("[Downloading video(s)]")

    videoLinks = GetVideoLinks(isPlaylist, links)
    DownloadVideos(videoLinks, videoFormat, args.downloadpath)

def GetVideoLinks(isPlaylist, links):
    if isPlaylist == False:
        return links

    urls = []
    for link in links:
        playlist_urls = Playlist(link)

        for url in playlist_urls:
            urls.append(url)
    
    return urls

def DownloadVideos(links, videoFormat, downloadpath):
    pathToDownload = f"{downloadpath}/{videoFormat}"
    print(f"Download location: {pathToDownload}\n")
    
    for link in links:
        video = YouTube(link)

        try:
            if not path.exists(pathToDownload):
                mkdir(pathToDownload)

            video.streams.filter(only_audio=True) if videoFormat == "mp3" else video.streams.filter(file_extension="mp4")
            stream = video.streams.first()
        except Exception as e:
            print(f"Wrong paremeters for {video.title}. Moving on. Reason: {e}")
            continue

        try:
            videoTitle = re.sub(r"[^\w\s-]", "", video.title.lower())
            print(f"Downloading... {videoTitle} @ {link}")
            fileName = f"{videoTitle}.{videoFormat}"
 
            stream.download(pathToDownload, fileName, None, True, None, 5)
            print(f"Download completed successfully!")
        except Exception as e:
            print(f"Download failed. Moving on. Reason: {e}")
            continue

    print("Downloads finished.")
    sleep(4)

Init()