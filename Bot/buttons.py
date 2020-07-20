from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove


def get_keyboard_tracks1(user_request):
    """
    Keyboard with songs and the button "next"
    """
    keyboard = [[]]
    for i in user_request[0:8]:
        button = InlineKeyboardButton(text=i, callback_data='cb_' + i)
        keyboard = keyboard + [[button]]

    button_next = InlineKeyboardButton(text='Дальше ➡', callback_data='cb_' + 'next')
    keyboard = keyboard + [[button_next]]
    return InlineKeyboardMarkup(keyboard, resize_keyboard=True)


def get_keyboard_tracks2(user_request):
    """
    Keyboard with songs and the button "previous"
    """
    keyboard = [[InlineKeyboardButton(text='⬅ Назад', callback_data='cb_' + 'previous')]]
    for i in user_request[8:16]:
        button = InlineKeyboardButton(text=i, callback_data='cb_' + i)
        keyboard = keyboard + [[button]]
    return InlineKeyboardMarkup(keyboard, resize_keyboard=True)

def admin_keyboard():
    """
    Keyboard for Admin's panel
    """
    return ReplyKeyboardMarkup([['Отправить сообщение', 'Все пользователи']])
