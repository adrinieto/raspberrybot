import logging

log = logging.getLogger(__name__)

EMOJI_DOWN = "\u2B07"
EMOJI_UP = "\u2B06"


class TorrentStatus:
    STOPPED = 0
    IDLE = 1
    DOWNLOADING = 2
    SEEDING = 3
    UP_AND_DOWN = 4
    QUEUED = 5

    conversion_from_string = {"Stopped": STOPPED,
                              "Idle": IDLE,
                              "Downloading": DOWNLOADING,
                              "Seeding": SEEDING,
                              "Up & Down": UP_AND_DOWN,
                              "Queued": QUEUED,
                              }

    conversion_to_string = {v: k for k, v in conversion_from_string.items()}

    @classmethod
    def string_to_status(cls, string):
        return cls.conversion_from_string[string]


class Torrent:
    def __init__(self, *args):
        log.debug("Torrent args: %s", args)
        self.id = int(args[0])
        self.done = args[1]
        self.downloaded = args[2]
        self.eta = args[3]
        self.up = args[4]
        self.down = args[5]
        self.ratio = args[6]
        self.status = TorrentStatus.string_to_status(args[7])
        self.name = args[8]

    def format_telegram(self):
        string = "*[{t.id}]* _{t.name}_\n"
        string += "     {t.done} "
        if self.done != "100%":
            string += "(%s) " % self.eta
        if self.status in [TorrentStatus.DOWNLOADING, TorrentStatus.SEEDING, TorrentStatus.UP_AND_DOWN]:
            string += "| " + EMOJI_UP + "{t.up:^10}"
        if self.status in [TorrentStatus.DOWNLOADING, TorrentStatus.UP_AND_DOWN]:
            string += "| " + EMOJI_DOWN + "{t.down:^10}"
        return string.format(t=self)

    def __eq__(self, other):
        if isinstance(other, Torrent):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return 'Torrent(id=%s,name="%s")' % (self.id, self.name)

    def __str__(self):
        return "[{t.id}] {t.name} {t.status} {t.done} ↑{t.up} ↓{t.down} ETA {t.eta}".format(t=self)
