from Bot.admin import admin, admin_see_users, send_message_start, text_approval, admin_approval, admin_dontknow
from Bot import settings
from Bot.buttons import get_keyboard_tracks1, get_keyboard_tracks2
from Bot.analytics import analytics_bot
from Bot.music_parsing import get_url, parse
import logging
import os
import urllib.request
#from telegram import Audio, Bot, Message, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

logging.basicConfig(filename='bot.log', level=logging.INFO)

# Response-phrases
phrase_1 = 'Хм.... Вот что я нашел по твоему запросу :\n'  # 43
phrase_2 = 'Хм.... Еще несколько :\n'  # 23


def start(update, context):
    """
    Command 'Start' will result in an initial phrase.
    """
    print(f'Новый запрос от : {update.message.from_user}.')

    # Analytics
    #analytics_bot(user_info=update.message.from_user)

    update.message.reply_text(
        text=f'Привет, {update.message.from_user.first_name}. Напиши название песни или исполнителя',
    )


def request_from_user(update, context):  # every new message from user will create a request to search.
    """
    The function returns a list of songs based on user's request
    """
    # Analytics
    print(f'Запрос от : {update.message.from_user}.')
    analytics_bot(user_info=update.message.from_user)

    text = update.message.text
    context.user_data['request'] = update.message.text

    # Parsing data
    df = parse(get_url(text))

    request_result = {}
    for i in range(len(df.index)):
        request_result[df['target_tracks_target'][i]] = df['target_tracks_link'][i]
    context.user_data['request_result'] = request_result

    buttons_name = list(context.user_data['request_result'].keys())

    # Response to user with a list of songs
    update.message.reply_text(
        text=phrase_1 + text,
        reply_markup=get_keyboard_tracks1(buttons_name))


def button(update, context):
    """
    The function returns an interesting song or an updated list of songs
    """
    query = update.callback_query
    user_request = query.data

    if context.user_data['request'] == update.effective_message.text[-len(context.user_data['request']):]:
        if user_request == 'cb_next':
            buttons_name = list(context.user_data['request_result'].keys())

            query.edit_message_text(text=phrase_2 + context.user_data['request'],
                                    reply_markup=get_keyboard_tracks2(buttons_name))
        elif user_request == 'cb_previous':
            buttons_name = list(context.user_data['request_result'].keys())

            query.edit_message_text(
                text=phrase_1 + context.user_data['request'],
                reply_markup=get_keyboard_tracks1(buttons_name))
        else:
            track_target = user_request[3:]
            link = context.user_data['request_result'][track_target]

            # Downloading file to local computer, sending it to user and deleting it from local computer
            name = 'temporary_request/' + user_request[3:] + '.mp3'
            urllib.request.urlretrieve(link, filename=name)
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(name, 'rb'))
            os.remove(name)
    else:
        query.edit_message_text(text='Данный запрос больше не доступен. Начни сначала /start')


def main():
    """
    Bot's initialisation
    """
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks

    print('Start')
    updater = Updater(
        token=settings.Bot_key,
        request_kwargs=settings.PROXY,
        use_context=True
    )
    print(f'Бот запущен: {updater.bot.get_me()}.')


    admin_send_message=ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Отправить сообщение)$'), send_message_start), # ^ - начало строки, $ - конец строки,
        ],
        states={
            'admin_text': [MessageHandler(Filters.text, text_approval)],
            'admin_approval': [MessageHandler(Filters.regex('^(Да|Нет)$'), admin_approval)],  # | или
        },
        fallbacks=[CommandHandler('cancel', admin_dontknow)]
    )

    updater.dispatcher.add_handler(admin_send_message)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('admin', admin))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(Все пользователи)$'), admin_see_users))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=request_from_user))

    # Start the Bot
    logging.info('Бот стартовал')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
