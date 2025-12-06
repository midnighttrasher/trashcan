def handle(bot, user, channel, args=None):
    if user.lower() != bot.USER.lower():
        bot.send_message(channel, f"Hallo {user}. Willkommen im irc der blackflag crew, aktuell sind wir noch im Aufbau. Wenn mtrash hier nicht im Chat ist, wurde er per Pushbenachrichtung über deinen Besuch informiert. Schreibe, was du ihm sagen möchtest hier rein.")
