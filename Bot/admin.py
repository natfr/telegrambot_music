from Bot import settings
from Bot.buttons import admin_keyboard
from telegram import Bot
import os
import pandas as pd
from telegram import ReplyKeyboardMarkup ,ReplyKeyboardRemove
from telegram.ext import ConversationHandler


def admin(update, context):
    """
    Command 'Admin' will call in admin panel.
    """
    bot = Bot(
        token=settings.Bot_key,
        base_url=settings.Base_url,
    )

    if update.message.from_user.id==settings.Bot_admin:
        text = 'Привет, админ'
        bot.send_message(chat_id=update.message.from_user.id, text=text, reply_markup=admin_keyboard())
    else:
        text = 'У Вас нет доступа к Админ-панели'
        bot.send_message(chat_id=update.message.from_user.id, text=text)


def admin_see_users(update, context):
    """
    The function allows Admin to see the list of all users.
    """
    bot = Bot(
        token=settings.Bot_key,
        base_url=settings.Base_url,
    )

    if update.message.from_user.id == settings.Bot_admin:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), "chat_id.csv"), delimiter=",")
        all_users=[]
        for i in range(len(df.index)):
            user=str(df['Chat_id'][i])+' | '+ str(df['Username'][i])+' | '+str(df['Firstname'][i])+' | '+str(df['Lastname'][i])+' | '
            all_users.append(user)
        bot.send_message(chat_id=update.message.from_user.id, text='\n'.join(all_users))
    else:
        text = 'У Вас нет доступа к Админ-панели'
        bot.send_message(chat_id=update.message.from_user.id, text=text)


def send_message_start(update, context):
    """
    The function asks Admin to send an initial text of message to send it to all users.
    """
    if update.message.from_user.id == settings.Bot_admin:
        update.message.reply_text("Отправьте сообщение, которое бы Вы хотели отправить всем пользователям",
                                  reply_markup=ReplyKeyboardRemove())
        return 'admin_text'
    else:
        text = 'У Вас нет доступа к Админ-панели'
        bot.send_message(chat_id=update.message.from_user.id, text=text)
        return ConversationHandler.END


def text_approval(update, context):
    text_message = update.message.text
    context.user_data['admin_send_message'] = {'admin_text': text_message}
    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text(
        "Это то, что вы хотите отправить всем пользователям?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 'admin_approval'


def admin_approval(update, context):
    admin_answer = update.message.text

    bot = Bot(
        token=settings.Bot_key,
        base_url=settings.Base_url,
    )
    if admin_answer=='Да':

        # # Send message to all users
        # df = pd.read_csv(os.path.join(os.path.dirname(__file__), "chat_id.csv"), delimiter=",")
        # list_id = df['Chat_id'].values.tolist()
        # count = 0
        # for i in list_id:
        #     try:
        #         bot.send_message(chat_id=i, text=context.user_data['admin_send_message']['admin_text']),
        #         count = count + 1
        #     except:
        #         pass
        # print(count)

        bot.send_message(chat_id=settings.Bot_admin, text=context.user_data['admin_send_message']['admin_text'])
        return ConversationHandler.END
    else:
        bot.send_message(chat_id=settings.Bot_admin, text='Начни сначала /admin')
        return ConversationHandler.END


def admin_dontknow(update, context):
    update.message.reply_text('Вы вышли из режима admin. Нажмите /admin , чтобы снова войти')
    return ConversationHandler.END



