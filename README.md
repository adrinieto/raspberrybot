raspberrybot
=============

A bot to get info and interact with the Raspberry Pi.

 Currently the next functions are supported:
 - Get local and public ip
 - Uptime
 - Interact with Transmission:
  - Add a torrent
  - List all torrents and their status
  - View info about a torrent
  - Remove a torrent
  - Notification when a torrent ends downloading

The full list of commands supported are listed in [`commands_list.txt`](../master/commands_list.txt).

##### Security

The first user who calls the `/start` command is the only one who can use the bot, his user id is stored in `user_id.dat`. The user id is checked in every command so only one account can use the bot. Other users that send any command will receive the response "User not allowed".

##### Launch bot on startup

Add this in `/etc/rc.local` before `exit 0`:
```
cd /home/pi/raspberry-bot
./venv/bin/python3 raspberrybot.py &
```

#### Sample of usage

![](https://github.com/adrinieto/raspberrybot/blob/master/screenshots/telegram_sample.jpg)
