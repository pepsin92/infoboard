import os.path
import logging
from datetime import date

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
                self.type = 'image'
                self.duration = int(args[3])
                self.filename = 'pictures/' + filename

                if not os.path.isfile(self.filename):
                    raise ValueError('Picture "{0}" does not exist'
                        .format(self.filename))
            else:
                self.type = 'video'
                self.filename = 'videos/' + filename

                if not os.path.isfile(self.filename):
                    raise ValueError('Video "{0}" does not exist'
                        .format(self.filename))
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
