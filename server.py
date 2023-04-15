from Сonfig import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler

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


async def registration(update, context):
    await update.message.reply_text(
        "В каком городе вы живёте?")

    return 1


async def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    city = update.message.text
    otvet1.append(city)
    await update.message.reply_text(
        f"Сколько вам лет?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


async def second_response(update, context):
    # Это ответ на второй вопрос.
    # Мы можем использовать его во втором вопросе.
    years = update.message.text
    otvet1.append(years)
    await update.message.reply_text(
        f"Какие у вас увлечения?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 3

async def third_response(update, context):
    hobbies = update.message.text
    otvet1.append(hobbies)
    await update.message.reply_text(
        f"Загрузите своё фото.")
    return 4


async def four_response(update, context):
    # Ответ на третий вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    photo = update.message
    photo_list.append(photo)
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
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, four_response)]
        },
        fallbacks=[CommandHandler('stop', second_response)]
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