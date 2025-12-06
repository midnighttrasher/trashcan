def handle(bot, user, channel, args=None):
    if user.lower() != bot.USER.lower():
        bot.send_message(channel, f"Hello {user}. I luv u.")
