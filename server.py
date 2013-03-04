import glob
import sys
import time
import re
import logging
import infoboard
import os
from datetime import date
from infoboard.video import Video
from infoboard.videoplayer import VideoPlayer
from infoboard.watcher import Watcher
from watchdog.utils import read_text_file


class Infoboard:
    def __init__(self, watcher, player, schedule_dir):
        self.videos = {}
        self._setup_logging()
        watcher.set_callback(self.process_schedule)
        self.watcher = watcher
        self.player = player
        self.schedule_dir = schedule_dir

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
        self.process_all_schedules()
        self.watcher.start()
        self.player.play(self)

    def process_schedule(self, key, schedule):
        self.videos[key] = []
        for line in schedule.split('\n'):
            line = line.strip()
            if (not line) or line.startswith('#'): continue
            try:
                self.videos[key].append(infoboard.video.Video(line))
            except:
                pass

    def process_all_schedules(self):
        for filename in glob.glob(self.schedule_dir + '/*.txt'):
            filename = os.path.abspath(filename)
            self.process_schedule(filename, read_text_file(filename))


    def get_playlist(self):
        self.process_all_schedules()
        today = date.today()
        all_videos = []
        for key in sorted(self.videos.keys()):
            all_videos += self.videos[key]
        return [video.filename for video in all_videos
                if video.start_date <= today and video.end_date >= today]


if __name__ == "__main__":
    v = infoboard.videoplayer.VideoPlayer()
    w = infoboard.watcher.Watcher('schedule')
    ib = Infoboard(w, v, 'schedule')
    ib.run()
