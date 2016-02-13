import logging

log = logging.getLogger(__name__)


class Torrent:
    def __init__(self, *args):
        log.debug("Torrent args: %s", args)
        self.id = args[0]
        self.done = args[1]
        self.downloaded = args[2]
        self.eta = args[3]
        self.up = args[4]
        self.down = args[5]
        self.ratio = args[6]
        self.status = args[7]
        self.name = args[8]

    def format_telegram(self):
        return "[{t.id}] {t.name}\n   {t.status} | {t.done} | \u2B06{t.up:^10}  \u2B07{t.down:^10} | {t.eta}".format(
            t=self)

    def __repr__(self):
        return 'Torrent(id=%s,name="%s")' % (self.id, self.name)

    def __str__(self):
        return "[{t.id}] {t.name} {t.status} {t.done} ↑{t.up} ↓{t.down} ETA {t.eta}".format(t=self)
