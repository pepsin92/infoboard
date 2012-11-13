import sys
import time
import re
import logging
import os.path
import subprocess
from subprocess import PIPE
from datetime import date
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import read_text_file


class Video:
    def __init__(self, line):
        try:
            filename, y1, m1, d1, y2, m2, d2 = line.split(' ')
            filename = 'videos/' + filename
            if not os.path.isfile(filename):
                raise ValueError('Video "{0}" does not exist'.format(filename))
            self.filename = filename
            self.start_date = date(int(y1), int(m1), int(d1))
            self.end_date = date(int(y2), int(m2), int(d2))
            if (self.end_date - self.start_date).total_seconds() < 0:
                message = 'Video "{0}" has start date after end date.'.format(
                    filename)
                logging.getLogger('infoboard.video').warning(message)
        except ValueError as e:
            message = "Error:\n    " + str(e) + "\n"
            message += "in configuration on line:\n    " + line + "\n"
            logging.getLogger('infoboard.video').error(message)
            raise e


class VideoPlayer:
    def __init__(self, playlist_producer):
        self.playlist_producer = playlist_producer
        command = ['/usr/bin/mplayer',
                   # reads commands from stdin
                   '-slave',
                   # don't quit when there is no file to play
                   '-idle', 
                   # fullscreen
#                   '-fs', 
                   # no way to control mplayer in other way
                   '-input', 'nodefault-bindings:conf=/dev/null', 
                   # reuse same window for playing all videos
                   '-fixed-vo', 
                   # don't print progress
                   '-quiet', 
                   # prepend messages with their origin module
                   '-msgmodule', 
                   # we are interested just in one type of messags
                   '-msglevel', 'all=0:cplayer=4',
                  ]
        self.mp_process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    def play(self):
        while True:
            playlist = self.playlist_producer.get_playlist()
            for video in playlist:
                self.mp_process.stdin.write('loadfile '+video+' 1\n')
            pending_videos = len(playlist) * 2
            while pending_videos:
                line = self.mp_process.stdout.readline().strip()
                if line == "CPLAYER:": pending_videos -= 1
    
    def stop(self):
        pass

class Infoboard:
    def __init__(self, watcher, player, playlist_producer, schedule_file):
        self.videos = []
        self._setup_logging()
        watcher.set_callback(self.process_schedule)
        self.watcher = watcher
        self.playlist_producer = playlist_producer
        self.player = player
        self.schedule_file = schedule_file

    def _setup_logging(self):
        logger = logging.getLogger('infoboard')
        fh = logging.FileHandler('error.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

    def run(self):
        self.process_schedule(read_text_file(self.schedule_file))
        self.watcher.start()
        self.player.play()

    def process_schedule(self, schedule):
        self.videos = self._parse_schedule(schedule)
        self.playlist_producer.set_videos(self.videos)

    def _parse_schedule(self, text):
        videos = []
        for line in text.split('\n'):
            line = line.strip()
            if (not line) or line.startswith('#'): continue
            try:
                videos.append(Video(line))
            except ValueError:
                pass
        return videos

class PlaylistProducer:
    def __init__(self, videos=[]):
        self.videos = []

    def set_videos(self, videos):
        self.videos = videos

    def get_playlist(self): 
        return [video.filename for video in self.videos]

class Watcher:
    def __init__(self, filename, callback=lambda x: None):
        self.callback = callback 
        event_handler = FileSystemEventHandler()
        def handler(e):
            if e.src_path.endswith('/' + filename):
                self.callback(read_text_file(e.src_path))
        # this happens also when file is created
        event_handler.on_modified = handler
        self.observer = Observer()
        self.observer.schedule(event_handler, '.')

    def set_callback(self, cb):
        self.callback = cb

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()


if __name__ == "__main__":
    schedule_file = 'schedule.txt'
    pp = PlaylistProducer()
    v = VideoPlayer(pp)
    w = Watcher(schedule_file)
    ib = Infoboard(w, v, pp, schedule_file)
    ib.run()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        w.stop()
#    observer.join()
