#!/usr/bin/env python
from PyQt4.QtCore import QDateTime, QObject, QUrl, pyqtSignal, QFileSystemWatcher, QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView

import glob
import sys
import time
import re
import logging
import infoboard
import os
from datetime import date
from infoboard.video import Video

class Infoboard(object):
    def __init__(self, schedule_dir):
        self.schedule_dir = schedule_dir
        self.videos = {}
        self.playlist = []

        self.app = QApplication(sys.argv)

        self.view = QDeclarativeView()
        self.view.setSource(QUrl('scene.qml'))
        self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.viewRoot = self.view.rootObject()
        self.viewRoot.quit.connect(self.app.quit)
        self.viewRoot.finished.connect(self.show_next)

        self.view.setGeometry(100, 100, 400, 240)
        self.view.showFullScreen()

        self.watcher = QFileSystemWatcher()

    def schedule_dir_changed(self, filename):
        self.process_all_schedules()
        self.playlist = []

    def run(self):
        self.watcher.addPath(self.schedule_dir)
        self.watcher.directoryChanged.connect(self.schedule_dir_changed)
        self.process_all_schedules()
        self.show_next()
        self.app.exec_()

    def process_schedule(self, key, fobj):
        self.videos[key] = []
        for line in fobj:
            line = line.strip()
            if (not line) or line.startswith('#'): continue
            try:
                self.videos[key].append(Video(line))
            except:
                pass

    def process_all_schedules(self):
        for filename in glob.glob(self.schedule_dir + '/*.txt'):
            filename = os.path.abspath(filename)
            with open(filename, 'rb') as f:
                self.process_schedule(filename, f)

    def show_next(self):
        item = self.playlist_next()
        if not item:
          return

        if item.type == 'image':
            self.viewRoot.showImage(item.filename)
            self.viewRoot.update()
            QTimer.singleShot(item.duration * 1000, self.show_next)
        elif item.type == 'video':
            self.viewRoot.showVideo(item.filename)

    def playlist_next(self):
        if len(self.playlist) == 0:
            self.process_all_schedules()
            today = date.today()
            all_videos = []
            for key in sorted(self.videos.keys()):
                all_videos += self.videos[key]
            self.playlist = [video for video in all_videos
                    if video.start_date <= today and video.end_date >= today]
        if len(self.playlist) == 0:
            return None
        return self.playlist.pop(0)

if __name__ == "__main__":
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

    Infoboard('schedule').run()
