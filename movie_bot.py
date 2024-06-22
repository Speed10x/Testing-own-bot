import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Replace with your bot token and OMDb API key
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OMDB_API_KEY = 'YOUR_OMDB_API_KEY'

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /search <movie_name> to find movies.')

def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please specify a movie name.')
        return
    
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
        
        query.edit_message_text(text=message, parse_mode='Markdown')
    else:
        query.edit_message_text(text='Movie details not found.')

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
