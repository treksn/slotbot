# Telegram Bot for Bouldering Hall Booking System

This is a Telegram bot designed to automatically book slots for a bouldering hall booking system. The bot has the following features:

1. **Show Available Slots:** The bot can show the available slots for a specific day and time. Users can query the bot to see which slots are available, and the bot will display the list of available slots.

2. **Book a Slot:** The bot can book a slot for a specific day and time. Users can request the bot to book a slot, and the bot will automatically reserve the slot in the bouldering hall booking system.

3. **Set Up an Alarm:** The bot allows users to set up an alarm for a specific day and time if a slot becomes available when it is already booked out. This feature will notify the user when a slot becomes available and automatically book the slot for them.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bouldering-bot.git
cd bouldering-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```	

3. Set up environment variables:
Create a file named .env in the root directory of the project and add the following variables:

```makefile
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
BOULDERING_URL=YOUR_BOULDERING_BOOKING_SYSTEM_URL
```

4. Run the bot:
    
```bash
python bot.py
```

## Usage
Once the bot is running, users can interact with it via the Telegram app.

## Commands
- `/start`: Displays a welcome message and instructions on how to use the bot.
- `/available [date] [time]`: Shows the available slots for a specific day and time. Example usage: `/available 2023-02-20 16:00`
- `/book [date] [time]`: Books a slot for a specific day and time. Example usage: `/book 2023-02-20 16:00`
- `/alarm [date] [time]`: Sets up an alarm for a specific day and time if a slot becomes available. Example usage: `/alarm 2023-02-20 16:00`



## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues if you encounter any bugs or have suggestions for new features.