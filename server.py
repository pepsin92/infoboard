import sys
import time
import logging
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from watchdog.utils import read_text_file 


class VideoPlayer():
	def restart():
		pass

	def stop():
		pass

	def set_playlist(playlist):
		pass

class Infoboard():
	def Infoboard(watcher, player):
		pass

	def run():
		pass

class Watcher():
	def watch(filename, callback):
		pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = FileSystemEventHandler()

    def handler(y):
        if re.search("/[^/]+\\.txt$", y.src_path):
		print read_text_file(y.src_path)

    event_handler.on_created = handler
    event_handler.on_modified = handler

    observer = Observer()
    observer.schedule(event_handler, '.')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
