from telegram.ext import *
import os
import openai

TOKEN = "telegram bot token"
openai.api_key = "open ai key"

async def start_command(update, context):
    await update.message.reply_text("Hey there! I'm Venture.")

async def help_command(update, context):
    await update.message.reply_text("Available Commands are:\n\n1. /search - Google something\n2. /gpt - Talk to Chatbot\n3. /gimage - Generate an AI image with GPT")

def handle_response(text: str) -> str:
    return f'What do you mean {text} , maybe try /help?'

async def handle_message(update, context):
    text = str(update.message.text)
    response = handle_response(text)

    await update.message.reply_text(response)
    print(f"User ({update.message.chat_id}) says: '{text}")

#command the search queries over google
async def search_command(update,context):
    from googlesearch import search
    user_input = " ".join(context.args)
    for j in search(user_input, tld="co.in", num=1, stop=1, pause=0):
        await update.message.reply_text(f'The Top search I could find was\n{j}')

#openAI to telegram bot
async def chatgpt_command(update,context):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=" ".join(context.args),
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
)
    await update.message.reply_text(response.choices[0].text)
    print(f"User ({update.message.chat_id}) says: '{context.args}")

#openAI image generator to telegram bot
async def chatgpt_image_command(update,context):
    response = openai.Image.create(
        prompt=" ".join(context.args),
        n=1,
        size="1024x1024"
)
    #image_url = response['data'][0]['url']
    await update.message.reply_photo(response['data'][0]['url'])


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    #commands
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('search', search_command))
    application.add_handler(CommandHandler('gpt', chatgpt_command))
    application.add_handler(CommandHandler('gimage', chatgpt_image_command))
    #application.add_handler(CommandHandler('image', google_image_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # run bot
    application.run_polling(1.0)
    application.idle()






