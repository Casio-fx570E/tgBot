from config import TOKEN
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
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
    await update.message.reply_text(update.message.text)


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
    if language == 'en':
        await update.message.reply_html(
            f"Hi, {user.mention_html()}! I'm a telegram bot to find someone to talk to, click 'help' to get information about me"
        )
    else:
        await update.message.reply_html(
            f"Привет, {user.mention_html()}! Я telegram-бот, чтобы найти собеседника, наберите '/help', чтобы получить информацию обо мне"
        )

async def help_command(update, context):
    language = update.effective_user.language_code
    if language == 'en':
        await update.message.reply_text("I'm helpless for now, but then there will be functions...")
    else:
        await update.message.reply_text("Я, пока-что, беспомощный, но потом будут функции...")


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
    # Запускаем приложение.
    application.run_polling()

    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()



