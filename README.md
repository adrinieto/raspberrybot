raspberrybot
=============

A bot to get info and interact with the Raspberry Pi.

 Currently the next functions are supported:
 - Get local and public ip
 - Add and list torrents downloading in Transmission

A full list of commands supported are listed in [`commands_list.txt`](../master/commands_list.txt).

##### Security

Only the first user who calls the `/start` command can use the Bot. The user id is stored in `user_id.dat`. If others
users call any command the response will be "User not allowed"

##### Launch Bot on startup

Add this in `etc/rc.local` before `exit 0`:
```
cd /home/pi/raspberry-bot
./venv/bin/python3 raspberrybot.py &
```

#### Sample

![](https://github.com/adrinieto/raspberrybot/blob/master/screenshots/telegram_sample.jpg)
