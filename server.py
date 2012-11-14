import sys
import time
import re
import logging
from infoboard import PlaylistProducer, Video, VideoPlayer, Watcher
from watchdog.utils import read_text_file


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
