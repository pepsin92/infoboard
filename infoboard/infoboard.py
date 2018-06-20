from PyQt5.QtWidgets import QWidget, QApplication
from infoboard.scheduler import Scheduler


class Infoboard(QApplication):
    """ Application window"""
    def __init__(self, schedule_dir, name='', args=[]):
        super().__init__(args)
        self.scheduler = Scheduler(schedule_dir, name)

    def run(self):
        # self.scheduler.show()
        self.scheduler.showFullScreen()
        return self.exec()
