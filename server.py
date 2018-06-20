from infoboard import Infoboard

import logging
import sys


if __name__ == '__main__':

    lg = logging.getLogger('infoboard.scheduler')
    lg.setLevel(logging.INFO)
    lg.addHandler(logging.StreamHandler())

    exit(Infoboard('schedule', args=sys.argv).run())
