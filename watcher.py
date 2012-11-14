from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import read_text_file

class Watcher:
    """Executes provided function when chosen file changes."""
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
