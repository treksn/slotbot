from telegram.ext import Application, CommandHandler
import configparser
import slots

# Get config
config = configparser.ConfigParser()
config.read('config.ini')

# '/book $date_time$' to book a slot.

# Define a function to handle the /hello command
async def hello(update, context):
    message = "Welcome to the BoulderGarten Booking Bot. You can use the following commands:\n\n /check date_time - Checks free slots. \n\ndate_time must be in the format <b><i>dd</i></b>, <b><i>ddhhmm</i></b> or <b><i>ddhh</i></b> -> e.g. <b><i>mo</i></b>, <b><i>mi14</i></b> or <b><i>sa2030</i></b>"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML')

# Define a function to handle the /available command
async def check(update, context):
    if len(context.args) > 0:
        message = slots.get_slots(context.args[0])    
    else:
        message = 'Please provide a date_time, for example:\n/check mi14'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define a function to handle the /book command
# async def book(update, context):
#     date = context.args[0]
#     time = context.args[1]
#     # TODO: Implement logic to book the selected slot
#     message = f"Booked slot for {date} at {time}"
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define a function to handle the /alarm command
# async def auto_book(update, context):
#     date = context.args[0]
#     time = context.args[1]
#     # TODO: Implement logic to automatically book a slot if it becomes available again
#     message = f"Alarm set up for {date} at {time}"
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    # Get telegram token
    token = config.get('credentials', 'telegram_token')

    # Create a new Telegram bot using the token provided by BotFather
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("hello", hello))
    application.add_handler(CommandHandler("check", check))
    # application.add_handler(CommandHandler("book", book))
    # application.add_handler(CommandHandler("alarm", auto_book))

    application.run_polling()

# RUN
main()