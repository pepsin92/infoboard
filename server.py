import sys
import time
import re
import logging
import os.path
import subprocess
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
				message = 'Video "{0}" has start date after end date.'.format(filename)
				logging.getLogger('infoboard.video').warning(message)
		except ValueError as e:
			message = "Error:\n    " + str(e) + "\n"
			message += "in configuration on line:\n    " + line + "\n"
			logging.getLogger('infoboard.video').error(message)
	
	

class VideoPlayer:
	def __init__(self):
		subprocess.Popen(['/usr/bin/mplayer', '-slave', '-idle', '-fixed-vo', '-identify', '-fs'])

	def restart(self):
		pass

	def stop(self):
		pass

	def set_playlist(self, playlist):
		pass

class Infoboard:
	def __init__(self, watcher, player):
		self.videos = []
		self._setup_logging()

	def _setup_logging(self):
		logger = logging.getLogger('infoboard')
		fh = logging.FileHandler('error.log')
		fh.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		logger.addHandler(fh)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		logger.addHandler(ch)

	def run(self):
		pass

	def process_schedule(self, schedule):
		self._parse_schedule(schedule)
	
	def _parse_schedule(self, text):
		for line in text.split('\n'):
			line = line.strip()
			if (not line) or line.startswith('#'): continue
			self.videos.append(Video(line))

class Watcher:
	def __init__(self, filename, callback):
    		event_handler = FileSystemEventHandler()
		def handler(e):
			if e.src_path.endswith('/' + filename):
				callback(read_text_file(e.src_path))
		event_handler.on_modified = handler # this happens also when file is created
		self.observer = Observer()
		self.observer.schedule(event_handler, '.')
		self.observer.start()

	def stop(self):
		self.observer.stop()


if __name__ == "__main__":
	ib = Infoboard(None, None)
	v = VideoPlayer()
	w = Watcher('schedule.txt', ib.process_schedule)

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		w.stop()
#    observer.join()
