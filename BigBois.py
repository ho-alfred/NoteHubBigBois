pip install python-telegram-bot

import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence

token = ['Insert API key here']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

maindict = {}

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Sorry! Unable to process {}".format(context.error))
    
    
def add_note(update, context): # user_input: /new mat.int.2 'text'
    subject_input = str(update.message.text).split(' ')
    key = subject_input[1]
    value = subject_input[2:]
    update.message.reply_text('Your input: ' + ' '.join(subject_input[1:]))
    maindict[key] = " ".join(value)    
    
def listing(update, context):
    result = ", ".join(maindict.keys())
    update.message.reply_text("Your codes: " + result)
    
def get_note(update, context): #/get math.int.2
    user_input = update.message.text.split(" ")
    retrieved = maindict[str(user_input[1])]
    update.message.reply_text('Your results:' + "\n" + retrieved)
    
    
def main():
    """Start the bot."""
    
    persist = PicklePersistence(filename='BigBoisdata')   

    updater = Updater(token, persistence=persist, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('add', add_note))
    dp.add_handler(CommandHandler('get', get_note))
    dp.add_handler(CommandHandler('list', listing))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()    
    
    updater.idle()

if __name__ == '__main__':
    main()
