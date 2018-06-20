from PyQt5.QtCore import QDateTime, QFileSystemWatcher
from PyQt5.QtWidgets import QStackedWidget

from infoboard.widgets import BusStopWidget, ImageWidget, VideoWidget

from os.path import abspath, isfile
import glob
import logging


class Scheduler(QStackedWidget):
    """ Parses all the schedules and manages content switching

        Scheduler class manages loading of schedules, filtering by infoboard name,
        creation of final schedule and
    """
    def __init__(self, schedule_dir, name=None):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.schedule_dir = schedule_dir
        self.name = name

        self.logger.info('Initializing scheduler \'{}\' on folder \'{}\''.format(name, schedule_dir))

        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.schedule_dir)
        self.watcher.directoryChanged.connect(self.schedule_dir_changed)
        self.schedule = None
        self.process_all_schedules()

    def schedule_dir_changed(self, filename):
        self.process_all_schedules()

    def process_all_schedules(self):
        schedules = []
        for fn in glob.glob(self.schedule_dir + '/*.txt'):
            with open(fn) as f:
                schedules.append(Schedule(f, callback=self.next_widget))

        self.logger.info('schedules loaded: ' + str(schedules))
        self.schedule = None

        for s in schedules:
            if self.name is None or self.name.startswith(s.name):
                if self.schedule is None:
                    self.schedule = s
                else:
                    self.schedule.playlist.extend(s.playlist)

        if self.schedule is None:
            self.logger.info('No valid schedule found')
            exit(0)

        self.reload_widgets()
        self.next_widget()

    def reload_widgets(self):
        for widget in self.schedule.playlist:
            self.addWidget(widget)

    def next_widget(self):
        if self.schedule is None:
            self.logger.warning('No schedule to select from')
            return

        widget = self.schedule.next_widget()
        self.logger.debug('Next widget: {}'.format(widget))
        self.setCurrentWidget(widget)
        try:
            widget.activate()
        except AttributeError:
            pass


class Schedule:
    """ Responsible for loading and parsing a single schedule file.

        For file format see schedules/schedule.example
        Skips image/video files that are not found in respective folders
    """
    def __init__(self, f, callback=None):
        self.name = ''
        self.playlist = []
        self.active = []

        for line in f:
            if line.startswith('#'):
                continue

            if line.startswith('@'):
                line = line[1:]

                if line.startswith('name'):
                    line = line[4:].strip()
                    self.name = line
                    continue

                if line.startswith('bus'):
                    _, bus_id, bt, et, timeout = line.split()
                    timeout = int(timeout)
                    self.playlist.append(BusStopWidget(bus_id, timeout=timeout, callback=callback))
                    self.playlist[-1].set_times(bt, et)

                if line.startswith('image'):
                    _, url, bt, et, timeout = line.split()
                    timeout = int(timeout)
                    img_url = abspath('pictures/' + url)
                    if not isfile(img_url):
                        continue
                    self.playlist.append(ImageWidget(img_url, timeout=timeout, callback=callback))
                    self.playlist[-1].set_times(bt, et)

                if line.startswith('video'):
                    _, url, bt, et = line.split()
                    video_url = abspath('videos/' + url)
                    if not isfile(video_url):
                        continue
                    self.playlist.append(VideoWidget(video_url, callback=callback))
                    self.playlist[-1].set_times(bt, et)

    def __str__(self):
        return '<infoboard.scheduler.Schedule, size {}>'.format(len(self.playlist))

    def __repr__(self):
        return '<infoboard.scheduler.Schedule {}>'.format(self.playlist)

    def next_widget(self, retry=False):
        while len(self.active) > 0:
            next = self.active.pop()
            if next.is_actual():
                return next
        if len(self.active) == 0 and retry:
            return None
        self.active = list(reversed(self.playlist))
        return self.next_widget(retry=True)
