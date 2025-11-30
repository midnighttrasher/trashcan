# trashcan IRC Bot

A simple, extendable IRC bot

---

## Status

The bot is **fully functional** and supports:

- SSL connection to any IRC server  
- NickServ authentication  
- Automatic channel join  
- Handling `!commands` from the channel or private message  
- Background jobs (e.g., periodic tasks like setting the topic)

---

## Configuration

Edit the `config.txt` file:

```ini
HOST=irc.example.net
PORT=6697
CHANNEL=#yourchannel
NICK=trashcan_bot
PW=yourpassword
FUNCS=ping,help
JOBS=settopic,3600;rallo,1337;
NOTIFY=tg,mail
```

- `FUNCS` loads interactive commands (triggered via `!command`)
- `JOBS` defines periodic background tasks:  
  Example: `settopic,600;` runs `jobs/settopic.py` every 600 seconds
- `NOTIFY` support is **planned but not yet implemented**

---

## Extending Functionality

To add a new command, place a `yourcommand.py` inside the `funcs/` folder:

```python
# funcs/ping.py
def handle(bot=None, user=None, channel=None, args=None):
    bot.send_message(channel, "pong.")
```

To use it in IRC:

```
!ping
```

To add a new job, place a file in `jobs/` with a `handle(t, channel, bot=None)` function.  
It will be launched in a separate thread.

---

## Planned Features

- Notify module support (e.g. Telegram, email)  

---


Built by mtrash
blackflagcrew.net
