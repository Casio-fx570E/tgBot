from Сonfig import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, Updater
# import wget
import sqlite3

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.

# Запускаем логгирование


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
otvet1 = list()
photo_list = []


# to_DB для добавления в баззу данных
# name то значение
# what_to_add это то что добавляется(возраст город имя и информация)
# user пользователь у которого меняются значения в бд
def to_DB(name, what_to_add, user):
    if what_to_add == 'city':
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = "UPDATE Profile SET city = '" + name + "' WHERE user =" + user
        res = cur.execute(result)
        con.commit()
        con.close()
    elif what_to_add == 'age':
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = "UPDATE Profile SET age = '" + name + "' WHERE user =" + user
        res = cur.execute(result)
        con.commit()
        con.close()
    elif what_to_add == 'info':
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = "UPDATE Profile SET info = '" + name + "' WHERE user =" + user
        res = cur.execute(result)
        con.commit()
        con.close()
    elif what_to_add == 'name':
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = "UPDATE Profile SET name = '" + name + "' WHERE user =" + user
        res = cur.execute(result)
        con.commit()
        con.close()


async def start(update, context):
    user = update.effective_user
    language = update.effective_user.language_code
    if language == 'en':
        await update.message.reply_html(
            f"Hi, {user.mention_html()}! I'm a telegram bot to find someone to talk to, click 'help' to get information about me",
            reply_markup=markup
        )
    if language == 'ru':
        await update.message.reply_html(
            f"Привет, {user.mention_html()}! Я telegram-бот, чтобы найти собеседника, наберите '/help', чтобы получить информацию обо мне",
            reply_markup=markup
        )


async def help_command(update, context):
    language = update.effective_user.language_code
    if language == 'en':
        await update.message.reply_text("I'm helpless for now, but then there will be functions...")
    else:
        await update.message.reply_text(
            "Здравствуйте, я бот знакомств. Здесь вы можете найти себе знакомства, заполнив анкету."
            "Для начала напишите /registration, если вы захотите убрать кнопки напишите - /close",
            reply_markup=markup)


# def image_handler(update, context):
#     file = update.message.photo[0].file_id
#     obj = context.bot.get_file(file)
#     obj.download()

async def registration(update, context):
    flag = False
    user = update.effective_chat.id
    con = sqlite3.connect('Tg-bot-DB.db')
    cur = con.cursor()
    result = "SELECT user FROM Profile"
    res = cur.execute(result).fetchall()
    print(user)
    print(res)
    print(user not in res[0])
    for i in range(len(res)):
        if user in res[i]:
            print(res[i])
            print(user in res[i])
            flag = True
    if flag is False:
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = f"INSERT INTO Profile(user) VALUES({user})"
        res = cur.execute(result)
        con.commit()
    con.close()
    await update.message.reply_text(
        "В каком городе вы живёте?")

    return 1


async def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    city = update.message.text
    user = update.effective_chat.id
    to_DB(str(city), 'city', str(user))
    await update.message.reply_text(
        f"Сколько вам лет?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


async def second_response(update, context):
    # Это ответ на второй вопрос.
    # Мы можем использовать его во втором вопросе.
    user = update.effective_chat.id
    years = update.message.text
    to_DB(str(years), 'age', str(user))
    await update.message.reply_text(
        f"Какие у вас увлечения?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 3


async def third_response(update, context):
    hobbies = update.message.text
    user = update.effective_chat.id
    to_DB(str(hobbies), 'info', str(user))
    await update.message.reply_text(
        "Назовите своё настоящее имя")
    return 4


async def fourth_response(update, context):
    name = update.message.text
    user = update.effective_chat.id
    to_DB(str(name), 'name', str(user))
    await update.message.reply_text(f"Регистрация успешно пройдена!")
    return ConversationHandler.END


async def fifth_response(update, context):
    # Ответ на третий вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    file = update.message.photo[-1].file_id
    # obj = context.get_file(file)
    # obj.download()
    otvet1.append(file)
    await update.message.reply_text(f"Регистрация успешно пройдена!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def anketa(update, context):
    await update.message.reply_text(
        ", ".join(otvet1),
        reply_markup=markup)


async def close(update, context):
    await update.message.reply_text(
        'Клавиатура скрыта',
        reply_markup=markdown
    )


btn1 = "Регистрация 🧩"
reply_keyboard = [['/registration', '/search'],
                  ['/anketa', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markdown = ReplyKeyboardRemove()


async def search(update, context):
    await update.message.reply_text(
        "Поиск собеседника.")


def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('registration', registration)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)]
        },
        fallbacks=[CommandHandler('stop', fourth_response)]
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("anketa", anketa))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
