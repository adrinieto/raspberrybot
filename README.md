raspberry-bot
=============

A small bot to get info from the Raspberry Pi.
The commands supported are listed in [`commands_list.txt`](../master/commands_list.txt).

##### Usage

Only the first user who calls the `/start` command can use the Bot. The user id is stored in `user_id.dat`. If others
users call any command the response will be "User not allowed"

#### Launch Bot on startup

Add this in `etc/rc.local` before `exit 0`:
```
cd /home/pi/raspberry-bot
./venv/bin/python3 raspberrybot.py &
```
