from сonfig import TOKEN
from telegram import ReplyKeyboardMarkup, User
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
import sqlite3


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text("Пожалуйста подождите, когда будут добавлены команды.")


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.


async def start(update, context):
    user = update.effective_user
    language = update.effective_user.language_code
    con = sqlite3.connect('tg-bot.db')
    cur = con.cursor()
    result = f"INSERT INTO user value {user}"
    res = cur.execute(result).fetchall()
    if language == 'en':
        await update.message.reply_html(
            f"Hi, {user.mention_html()}! I'm a telegram bot to find someone to talk to, click 'help' to get information about me",
            reply_markup=markup
        )
    else:
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
            "Для начала напишите /start")


async def registration(update, context):
    await update.message.reply_text(
        "Введите ваше имя")
    return 1


async def search(update, context):
    await update.message.reply_text(
        "Поиск друга.")


async def name_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    name = update.message.text
    con = sqlite3.connect('tg-bot.db')
    cur = con.cursor()
    result = f"INSERT INTO name value {name}"
    res = cur.execute(result).fetchall()
    await update.message.reply_text(
        f"Сколько вам лет?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


async def age_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    age = update.message.text
    con = sqlite3.connect('tg-bot.db')
    cur = con.cursor()
    result = f"INSERT INTO age value {age}"
    res = cur.execute(result).fetchall()
    await update.message.reply_text("Из какого вы города?")
    return 3  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def city_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    city = update.message.text
    con = sqlite3.connect('tg-bot.db')
    cur = con.cursor()
    result = f"INSERT INTO city value {city}"
    res = cur.execute(result).fetchall()
    await update.message.reply_text("Пожалуйста, расскажите о себе и о том кого вы здесь ищите")
    return 4  # Константа, означающая конец диалога.


async def info_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    info = update.message.text
    con = sqlite3.connect('tg-bot.db')
    cur = con.cursor()
    result = f"INSERT INTO info value {info}"
    res = cur.execute(result).fetchall()
    await update.message.reply_text("Спасибо за регистрацию, теперь вы можете искать собеседника!")
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


reply_keyboard = [['/registration', '/search']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

conv_handler = ConversationHandler(
    # Точка входа в диалог.
    # В данном случае — команда /start. Она задаёт первый вопрос.
    entry_points=[CommandHandler('registration', registration)],

    # Состояние внутри диалога.
    # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_response)],
        # Функция читает ответ на второй вопрос и завершает диалог.
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_response)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, city_response)],
        4: [MessageHandler(filters.TEXT & ~filters.COMMAND, city_response)]
    },

    # Точка прерывания диалога. В данном случае — команда /stop.
    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    # Создаём объект Application.
    application = Application.builder().token(TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("registration", registration))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(conv_handler)
    # Запускаем приложение.
    application.run_polling()

    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
