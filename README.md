# trashcan irc bot

_A simple, extendable IRC bot. Written in Python.

---

## Configuration

Just edit `configuration.txt`:

```ini
HOST=irc-server.example.com
PORT=6697
CHANNEL=#channel
NICK=trashcan_
PW=PASSWORD
```

---

## Extending Functionality

Edit this line in your config to load modules:

```ini
FUNCS=ping,help
```

The bot will then load `ping.py` and `help.py`.  
When you write `!ping` in IRC, it will execute `ping.py` – and so on.

---

## Future enhancements

- Permissions by (registered) user or user role
- Cronjob-like IRC command executions within the channel

---

