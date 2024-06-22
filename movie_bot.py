import os
import requests
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
BOT_PASSWORD = os.getenv('BOT_PASSWORD')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')

# In-memory storage for logo URL and other settings
settings = {
    'logo_url': '',
    'channel_link': CHANNEL_LINK
}

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK'

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        f'Welcome! Please login with /login <password>\n'
        f'Visit our channel for more movies: {settings["channel_link"]}'
    )


def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    

def login(update: Update, context: CallbackContext) -> None:
    if context.args and context.args[0] == BOT_PASSWORD:
        update.message.reply_text('Login successful! Use /search <movie_name> to find movies.')
    else:
        update.message.reply_text('Incorrect password. Please try again.')

def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please specify a movie name.')
        return

    # Simulate search animation
    update.message.reply_text('Searching...')
    time.sleep(2)  # Simulate a delay for animation

    url = f'http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}'
    response = requests.get(url).json()
    
    if response.get('Response') == 'True':
        movies = response.get('Search', [])
        buttons = [
            [InlineKeyboardButton(movie['Title'], callback_data=movie['imdbID'])]
            for movie in movies
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text('Select a movie:', reply_markup=reply_markup)
    else:
        update.message.reply_text('No movies found.')

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    movie_id = query.data
    
    url = f'http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}'
    response = requests.get(url).json()
    
    if response.get('Response') == 'True':
        title = response['Title']
        year = response['Year']
        rating = response['imdbRating']
        plot = response['Plot']
        poster = response['Poster']
        
        # Simulate a download link (you should integrate with an actual download source)
        download_link = f"http://example.com/download/{movie_id}"
        
        message = (
            f"Title: {title}\n"
            f"Year: {year}\n"
            f"IMDB Rating: {rating}\n"
            f"Plot: {plot}\n"
            f"[Poster]({poster})\n\n"
            f"[Download Link]({download_link})"
        )
        
        query.edit_message_text(text=message, parse_mode=ParseMode.MARKDOWN)
    else:
        query.edit_message_text(text='Movie details not found.')

def set_logo(update: Update, context: CallbackContext) -> None:
    if context.args and context.args[0].startswith('http'):
        settings['logo_url'] = context.args[0]
        update.message.reply_text('Logo URL set successfully!')
    else:
        update.message.reply_text('Please provide a valid URL.')

def edit_channel_link(update: Update, context: CallbackContext) -> None:
    if context.args and context.args[0].startswith('http'):
        settings['channel_link'] = context.args[0]
        update.message.reply_text('Channel link updated successfully!')
    else:
        update.message.reply_text('Please provide a valid URL.')

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/login <password> - Log in to the bot\n"
        "/search <movie_name> - Search for a movie\n"
        "/setlogo <logo_url> - Set the logo URL\n"
        "/editlink <channel_link> - Edit the channel link\n"
        "/help - Show this help message"
    )

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CommandHandler("setlogo", set_logo))
    dispatcher.add_handler(CommandHandler("editlink", edit_channel_link))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()

    # Start the Flask app for health check
    app.run(port=8080)

    updater.idle()
if __name__ == '__main__':
    main()
