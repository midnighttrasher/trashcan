import time

message = ":D"

def handle(t, channel, bot=None):
    while True:
        try:
            bot.send_message(channel, f"{message}")
        except Exception as e:
            print(f"[ERR] rallo-Job: {e}")
        time.sleep(t)
