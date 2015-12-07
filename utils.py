import subprocess
from urllib.request import urlopen


def get_local_ip():
    task = subprocess.Popen('ifconfig | grep "inet addr" | head -n 1| cut -d: -f2 | cut -d" " -f1', shell=True,
                            stdout=subprocess.PIPE)
    data = task.stdout.read()
    task.wait()
    return data.strip()


def get_public_ip():
    return urlopen("http://ipecho.net/plain").read()
