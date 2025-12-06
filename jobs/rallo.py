import time
import random

message = [';)', ':D', '._.', '🐘']

def handle(t, channel, bot=None):
    while True:
        try:
            bot.send_message(channel, f"{random.choice(message)}")
        except Exception as e:
            print(f"[ERR] rallo-Job: {e}")
        time.sleep(t)
