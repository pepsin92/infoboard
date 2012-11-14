class PlaylistProducer:
    """Generates playlist from supplied videos."""
    def __init__(self, videos=[]):
        self.videos = []

    def set_videos(self, videos):
        self.videos = videos

    def get_playlist(self): 
        return [video.filename for video in self.videos]
