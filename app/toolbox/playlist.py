from collections import deque


class SongPlaylist:
    def __init__(self):
        self.current_song = None
        self.next_song = None
        self.entries = deque()

    def __iter__(self):
        return iter(self.entries)

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_next_entry(self):
        ''' Grab next song to play once current song ends '''
        if not self.entries:
            return None

        self.entries.popleft()

        if self.entries:
            return self.entries[0]
