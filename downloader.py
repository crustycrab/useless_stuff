from urllib.request import urlopen, urlretrieve
from queue import Queue
import argparse
import threading
import json
import os
import sys

DIRECTORY = 'songs'


class StereoDoseHandler:

    def __init__(self, url, sample=None):
        self.url = url
        self.sample = sample
        self._songs = self.gen_songs()

    def gen_songs(self):
        with urlopen(self.url) as data:
            result = data.read().decode(sys.getdefaultencoding())

        start = "var songarray = "
        end = "var songids"
        songs = json.loads(
            result[result.find(start) + len(start):result.find(end)].rstrip()[:-1])
        if self.sample == None:
            return songs
        elif self.sample > 0:
            return [songs[i] for i in range(self.sample)]

    @property
    def songs(self):
        return self._songs

    @songs.setter
    def songs(self, stereodose):
        self._songs = stereodose.__dict__.get('_songs')


class GetSongThread(threading.Thread):

    def __init__(self, song):
        threading.Thread.__init__(self)
        self._song = song

    def run(self):
        download_song(self._song)


def download_song(song):
    filename = (song["artist"] + " - " + song["songtitle"]).replace("/", "-")
    client = "client_id=5a1f0425ba83c55eeb08b895d48eec9a"
    url = "https://api.soundcloud.com/tracks/%s/stream?%s" % (song["uuid"], client)

    if os.path.isfile(os.path.join(DIRECTORY, filename)):
        print("[U r already have dis] %s.." % filename)
        return
    try:
        print("[Downloading] %s.." % filename)
        urlretrieve(url, filename=os.path.join(DIRECTORY, filename))
    except ValueError as e:
        print("\t[Error, while downloading] %s, [deleting].." % filename)
        os.remove(os.path.join(DIRECTORY, filename))


def start(n_threads, q):
    while not q.empty():
        if n_threads != None:
            threads = []
            for i in range(n_threads):
                if not q.empty():
                    threads.append(GetSongThread(q.get()))
                    threads[i].start()
            for i in threads:
                i.join()
        else:
            download_song(q.get())


def main():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--songs',    action='store', type=int)
    parser.add_argument('-t', '--threads',  action='store', type=int)
    parser.add_argument('-p', '--playlist', action='store')

    args = parser.parse_args()
    if args.threads <= 0:
        args.threads = None

    stereodose = StereoDoseHandler(args.playlist, sample=args.songs)

    songs_queue = Queue()
    for i in stereodose.songs:
        songs_queue.put(i)

    start(args.threads, songs_queue)

if __name__ == "__main__":
    main()