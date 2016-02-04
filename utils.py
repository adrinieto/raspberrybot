# set encoding: utf-8
import logging
import subprocess
from urllib.request import urlopen

import config
from models import Torrent

log = logging.getLogger(__name__)


def system_call_with_response(command):
    task = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = task.stdout.read()
    task.wait()
    return output.decode("utf-8")


def get_local_ip():
    ip = system_call_with_response('ifconfig | grep "inet addr" | head -n 1| cut -d: -f2 | cut -d" " -f1')
    return ip.strip()


def get_public_ip():
    return urlopen("http://ipecho.net/plain").read()


def get_uptime():
    return system_call_with_response("uptime")


def torrent_add(url):
    command = "transmission-remote -n %s:%s -a '%s'" % (config.TRANSMISSION_USER, config.TRANSMISSION_PASSWORD, url)
    response = system_call_with_response(command)
    log.debug("Response from adding torrent: %s", response)
    return response


def torrent_list():
    command = "transmission-remote -n %s:%s -l" % (config.TRANSMISSION_USER, config.TRANSMISSION_PASSWORD)
    response = system_call_with_response(command)
    log.debug("Response from list torrents: %s", response)

    lines = response.split("\n")[1:-2]  # header in first line, summary and blank line at the end
    torrents = []
    for x in lines:
        words = [w for w in x.split("  ") if w]
        torrents.append(Torrent(*words))
    return torrents
