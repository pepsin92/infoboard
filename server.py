import sys
import time
import re
import logging
import infoboard
from datetime import date
from infoboard.video import Video
from infoboard.videoplayer import VideoPlayer
from infoboard.watcher import Watcher
from watchdog.utils import read_text_file


class Infoboard:
    def __init__(self, watcher, player, schedule_file):
        self.videos = []
        self._setup_logging()
        watcher.set_callback(self.process_schedule)
        self.watcher = watcher
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
        self.player.play(self)

    def process_schedule(self, schedule):
        self.videos = []
        for line in schedule.split('\n'):
            line = line.strip()
            if (not line) or line.startswith('#'): continue
            try:
                self.videos.append(infoboard.video.Video(line))
            except ValueError:
                pass

    def get_playlist(self):
        today = date.today()
        return [video.filename for video in self.videos
                if video.start_date <= today and video.end_date >= today]


if __name__ == "__main__":
    schedule_file = 'schedule.txt'
    v = infoboard.videoplayer.VideoPlayer()
    w = infoboard.watcher.Watcher(schedule_file, 'schedule')
    ib = Infoboard(w, v, 'schedule/'+schedule_file)
    ib.run()
