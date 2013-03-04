from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import read_text_file

class Watcher:
    """Executes provided function when chosen file changes."""
    def __init__(self, folder, callback=lambda x: None):
        self.callback = callback 
        event_handler = FileSystemEventHandler()
        def handler(e):
            path = e.src_path
            if path.endswith('.txt'):
                self.callback(path, read_text_file(path))
        # this happens also when file is created
        event_handler.on_modified = handler
        self.observer = Observer()
        self.observer.schedule(event_handler, folder)

    def set_callback(self, cb):
        self.callback = cb

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
