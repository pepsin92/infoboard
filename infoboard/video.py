import os.path
import logging
import subprocess
import multiprocessing 
from datetime import date
from subprocess import PIPE

def _runInSequence(first_process, second_process):
    """
    Spawns new process which manages to run two processes in sequence.
    These two are specified by subprocess.Popen args argument.
    """
    def runInProcess(first_process, second_process):
        proc = subprocess.Popen(first_process)
        proc.wait()
        subprocess.Popen(second_process)
        return
    process = multiprocessing.Process(target=runInProcess,
                                      args=(first_process, second_process))
    process.start()
    # returns immediately after the process starts
    return process

class Video:
    """Parses line containing description of a video.

    Line must contain filename followed by duration (two dates):
    test.avi 2012-01-12 2012-02-07
    In case of picture additional number (duration in seconds) is required:
    notice.jpg 2013-01-01 2014-12-31 30

    ValueError is thrown in case that specified video does not exists
    in 'videos' subfolder, picture is not in 'pictures' subfolder
    or there are not enough arguments.
    Possible reason is logged in 'infoboard.video' logger.
    """
    def __init__(self, line):
        try:
            args = line.split(' ')
            filename, first_day, last_day = args[:3]
            if len(args) == 4:
                duration = args[3]
                self._from_image(filename, duration)
                if not os.path.isfile('pictures/' + filename):
                    raise ValueError('Picture "{0}" does not exist'
                        .format(filename))
                filename = 'videos/' + filename + '.' + duration + '.avi'
            else:
                filename = 'videos/' + filename
                if not os.path.isfile(filename):
                    raise ValueError('Video "{0}" does not exist'
                        .format(filename))
            self.filename = filename
            self.start_date = date(*map(int, first_day.split('-')))
            self.end_date = date(*map(int, last_day.split('-')))
            if (self.end_date - self.start_date).total_seconds() < 0:
                message = 'Video "{0}" has start date after end date.'.format(
                    filename)
                logging.getLogger('infoboard.video').warning(message)
        except (ValueError, TypeError) as e:
            message = "Error:\n    " + str(e) + "\n"
            message += "in configuration on line:\n    " + line + "\n"
            logging.getLogger('infoboard.video').error(message)
            raise e

    def _from_image(self, filename, duration):
        """Created video from picture with requested duration
        unless it already exists."""
        videoname = filename + '.' + duration + '.avi'
        if os.path.isfile('/tmp/' + videoname):
            return
        if os.path.isfile('videos/' + videoname):
            return
        encode = ['/usr/bin/mencoder',
                  # reads commands from stdin
                  'mf://pictures/' + filename,
                  # don't quit when there is no file to play
                  '-o', '/tmp/' + videoname,
                  # fullscreen
                  '-ovc', 'lavc',
                  # no way to control mplayer in other way
                  '-lavcopts', 'vcodec=mjpeg', 
                  # reuse same window for playing all videos
                  '-fps', '1/' + duration,
                  # don't print progress
                  '-ofps', '30'
                 ]
        move_product = ['/bin/mv', '/tmp/' + videoname, 'videos/' + videoname]
        _runInSequence(encode, move_product)
        raise ValueError('Picture "{0}" is not yet encoded'.format(filename))
