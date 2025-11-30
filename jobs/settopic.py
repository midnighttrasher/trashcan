import time

topic = "Willkommen bei #bfc 🏴 | https://www.blackflagcrew.net"

def handle(t, channel, bot=None):
    while True:
        try:
            bot.sock.send(f"TOPIC {bot.CHAN} :{topic}\r\n".encode())
        except Exception as e:
            print(f"[ERR] Topic-Job: {e}")
        time.sleep(t)
