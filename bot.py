import telegram
import logging

from my_token import *


bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')