import subprocess
from urllib.request import urlopen

import config


def system_call_with_response(command):
    task = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = task.stdout.read()
    task.wait()
    return output


def get_local_ip():
    ip = system_call_with_response('ifconfig | grep "inet addr" | head -n 1| cut -d: -f2 | cut -d" " -f1')
    return ip.strip()


def get_public_ip():
    return urlopen("http://ipecho.net/plain").read()


def torrent_add(url):
    command = "transmission-remote -n %s:%s -a '%s'" % (config.TRANSMISSION_USER, config.TRANSMISSION_PASSWORD, url)
    response = system_call_with_response(command)
    return response


def torrent_list():
    command = "transmission-remote -n %s:%s -l" % (config.TRANSMISSION_USER, config.TRANSMISSION_PASSWORD)
    response = system_call_with_response(command)
    return response
