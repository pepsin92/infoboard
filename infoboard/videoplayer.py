import subprocess
from subprocess import PIPE

class VideoPlayer:
    """Uses mplayer to play playlists provided by playlist producer."""
    def __init__(self):
        """Starts mplayer process with correct arguments."""
        command = ['/usr/bin/mplayer',
                   # reads commands from stdin
                   '-slave',
                   # don't quit when there is no file to play
                   '-idle', 
                   # fullscreen
                   '-fs', 
                   # no way to control mplayer in other way
                   '-input', 'nodefault-bindings:conf=/dev/null', 
                   # reuse same window for playing all videos
                   '-fixed-vo', 
                   # don't print progress
                   '-quiet', 
                   # prepend messages with their origin module
                   '-msgmodule', 
                   # we are interested just in one type of messags
                   '-msglevel', 'all=0:cplayer=4',
                   # we won't use remote control
                   '-nolirc',
                   # keep orginal aspec ratio, don't stretch
                   '-noaspect',
                   # we don't want to use VDPAU video output
                   # because drivers may not be present
                   # (added to solve one error output, no idea what it is)
                   '-vo', 'xv',
                  ]
        self.mp_process = subprocess.Popen(command, stdin=PIPE, stdout=PIPE)

    def play(self, playlist_producer):
        """Plays provided playlists by playlist_producer.
        
        New playlist is obtained immidiately after current one is finished.
        """
        while True:
            playlist = playlist_producer.get_playlist()
            for video in playlist:
                self.mp_process.stdin.write('loadfile '+video+' 1\n')
            # we cannot distinguish between start and finish of video playback
            # event, so we have to count both
            pending_videos = len(playlist) * 2
            while pending_videos:
                line = self.mp_process.stdout.readline().strip()
                if line == "CPLAYER:": pending_videos -= 1
