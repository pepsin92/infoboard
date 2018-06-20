from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QColor, QPicture, QPixmap
from PyQt5.QtCore import QUrl, QTimer, QDate
from PyQt5.QtWidgets import QLabel
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import logging


class TimedSchedule:
    """ Manages dates to show content on screen
    """
    def __init__(self):
        self.start_date = None
        self.end_date = None

        self.logger = logging.getLogger('infoboard.widgets')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def set_times(self, beg, end):
        self.start_date = QDate(*map(int, beg.split('-')))
        self.end_date = QDate(*map(int, end.split('-')))
        if beg > end:
            self.logger.info("Begin date later than end date.")

    def is_actual(self):
        now = QDate.currentDate()
        # print(self.start_date, now, self.end_date, now <= self.end_date)
        if self.start_date is None:
            return True

        return self.start_date <= now <= self.end_date


class BusStopWidget(QWebEngineView, TimedSchedule):
    """ Shows bus schedule on screen

        Bus schedule is powered by imhd.sk. Bus stop id is internal IMHD ID.
        Circumvents cookie notice by removing it from HTML.
    """
    def __init__(self, stop_id, callback=None, timeout=None):
        super().__init__()
        self.stop_id = stop_id
        self.backgroundColor = QColor('black')
        self.setUrl(QUrl('https://imhd.sk/ba/online-zastavkova-tabula?z={}&skin=2&fullscreen=1'.format(stop_id)))
        self.loadFinished.connect(self.remove_cookie_notice)
        self.first_time = True
        self.timeout = timeout
        self.callback = callback
        if timeout is not None and callback is not None:
            self.timer = QTimer()
            self.timer.timeout.connect(self.callback)
            self.timer.setInterval(1000*self.timeout)
            self.timer.setSingleShot(True)

    def activate(self):
        if self.timeout is not None:
            self.timer.start()

    def __str__(self):
        return '<infoboard.widgets.BusStopWidget: {}>'.format(self.stop_id)

    def remove_cookie_notice(self, status):
        if status:
            self.page().runJavaScript("$('#cookieNotice').remove()")
            if self.first_time:
                self.first_time = False
                self.reload()

        else:
            # Page retrieval failed, show local landing page
            with open('infoboard/default_bus.html') as f:
                self.page().setHtml(f.read())

    def __call__(self):
        pass


class ImageWidget(QLabel, TimedSchedule):
    def __init__(self, image_url, callback=None, timeout=None):
        super().__init__()
        self.setScaledContents(True)
        # print(image_url)
        pix = QPixmap(image_url)
        # print(pix)
        self.setPixmap(pix.scaled(self.size()))

        self.timeout = timeout
        self.callback = callback
        if timeout is not None and callback is not None:
            self.timer = QTimer()
            self.timer.timeout.connect(self.callback)
            self.timer.setInterval(1000 * self.timeout)
            self.timer.setSingleShot(True)

    def activate(self):
        # print('img activated')
        if self.timeout is not None:
            self.timer.start()

    def mousePressEvent(self, QMouseEvent):
        print("image click")


class VideoWidget(QVideoWidget, TimedSchedule):
    def __init__(self, video_url, callback=None):
        super().__init__()
        self.url = video_url
        self.callback = callback

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_url)))
        self.player.setVideoOutput(self)
        self.player.error.connect(self.stopped)
        self.player.mediaStatusChanged.connect(self.stopped)

    def activate(self):
        self.play()

    def play(self):
        self.player.play()

    def stopped(self, state):
        # print(state, str(self.player.state()), QMediaPlayer.NoMedia, QMediaPlayer.EndOfMedia)
        if self.player.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.callback()

    def mousePressEvent(self, QMouseEvent):
        # print("video click")
        self.player.stop()
        self.player.setPosition(0)
        self.callback()
