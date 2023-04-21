from Сonfig import TOKEN, VK_TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, Updater
# import wget
import sqlite3, vk_api
import random
import tracemalloc

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
global friend

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
    elif what_to_add == 'username':
        con = sqlite3.connect('Tg-bot-DB.db')
        cur = con.cursor()
        result = "UPDATE Profile SET username = '" + name + "' WHERE user =" + user
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
            "Для начала напишите /registration или /registration_vk, если вы захотите убрать кнопки напишите - /close, чтоб вернуть /open",
            reply_markup=markup)


# def image_handler(update, context):
#     file = update.message.photo[0].file_id
#     obj = context.bot.get_file(file)
#     obj.download()


async def registration_from_vk(update, context):
    flag = False
    user = update.effective_chat.id
    con = sqlite3.connect('Tg-bot-DB.db')
    cur = con.cursor()
    result = "SELECT user FROM Profile"
    res = cur.execute(result).fetchall()
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
    await update.message.reply_text(
        "Пожалуйста, напишите свой id профиля во 'Вконтакте'.Не забудьте открыть его!(Всё, что после vk.com/...)")
    return 'vk'


async def vk_id_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    vk_id = update.message.text
    user_tg = update.effective_chat.id
    vk = vk_api.VkApi(token=VK_TOKEN)
    user = vk.method("users.get", {"user_ids": vk_id})  # вместо 1 подставляете айди нужного юзера
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    user_city = vk.method("users.get", {"fields": {"city": vk_id}})
    city = user_city[0]['city']['title']
    user_bdate = vk.method('users.get', {"fields": {"bdate": vk_id}})
    age = 2023 - int(str(user_bdate[0]['bdate']).split('.')[2])
    to_DB(str(fullname), 'name', str(user_tg))
    to_DB(str(city), 'city', str(user_tg))
    to_DB(str(age), 'age', str(user_tg))
    await update.message.reply_text(
        "Пожалуйста, напишите что-нибудь о себе(увлечения, хобби, интересы и др.).")
    return 'info_vk'


async def info_vk_response(update, context):
    hobbies = update.message.text
    user = update.effective_chat.id
    to_DB(str(hobbies), 'info', str(user))
    await update.message.reply_text(
        "Спасибо, теперь вы зарегестрировали.")
    return ConversationHandler.END


async def registration(update, context):
    flag = False
    user = update.effective_chat.id
    con = sqlite3.connect('Tg-bot-DB.db')
    cur = con.cursor()
    result = "SELECT user FROM Profile"
    res = cur.execute(result).fetchall()
    # print(user)
    # print(res)
    # print(user not in res[0])
    for i in range(len(res)):
        if user in res[i]:
            # print(res[i])
            # print(user in res[i])
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
    username = update.effective_user.name
    city = update.message.text
    user = update.effective_chat.id
    to_DB(str(username), 'username', str(user))
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
        f"Пожалуйста, напишите что-нибудь о себе(увлечения, хобби, интересы и др.).")
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
    return 5


async def fifth_response(update, context):
    user = update.effective_chat.id
    file_id = update.message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive(f'photo/Files{user}.jpg')
    await update.message.reply_text(f"Регистрация успешно пройдена!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def anketa(update, context):
    id = update.effective_chat.id
    # f = context.bot.send_document(document=open(f"photo/Files{id}.jpg" + update.effective_chat.id, 'rb'))
    connect = sqlite3.connect('Tg-bot-DB.db')
    cur = connect.cursor()
    res = f"""SELECT * FROM Profile " \
           f"WHERE user = {id}"""
    resultat = cur.execute(res).fetchall()
    # age = "".join(str(resultat[1]))
    for elem in resultat:
        await update.message.reply_text(
            f'Ваше имя: {elem[1]} 👑 \n'
            f'Ваш возраст: {elem[2]} 🌸 \n'
            f'Ваш город: {elem[3]} 🌇 \n'
            f'Ваше хобби: {elem[4]} 🪃 \n'
            f'Желаете что-то изменить?',
            reply_markup=markup)


async def close(update, context):
    await update.message.reply_text(
        'Клавиатура скрыта ⬇️',
        reply_markup=markdown
    )


async def open(update, context):
    await update.message.reply_text(
        f'Клавиатура открыта ⬆️',
        reply_markup=markup
    )


async def search(update, context):
    global friend
    age = 0
    spisok = []
    spisok1 = []
    city = str()
    id = update.effective_chat.id
    connect = sqlite3.connect('Tg-bot-DB.db')
    cur = connect.cursor()
    res = f"""SELECT * FROM Profile"""
    res_age = f"""SELECT age, city FROM Profile
                        WHERE {id} = user"""
    resultat_age = cur.execute(res_age).fetchall()
    resultat = cur.execute(res).fetchall()
    for i in resultat_age:
        age = i[0]
        city = i[1]
    for elem in range(len(resultat)):
        if age in resultat[elem] and id not in resultat[elem]:
            spisok.append(elem)
        elif city in resultat[elem] and id not in resultat[elem]:
            spisok1.append(elem)
    for elem in range(len(resultat)):
        if age in resultat[elem] and id not in resultat[elem]:
            randoms = random.choice(spisok)
            await update.message.reply_text(f'🎋 Анкеты потенциальных друзей 🎋\n'
                                            f'Имя 🏷: {resultat[randoms][1]} \n'
                                            f'Возраст 🧬: {resultat[randoms][2]} \n'
                                            f'Город 🌆: {resultat[randoms][3]} \n'
                                            f'Хобби 🤿: {resultat[randoms][4]}. \n', reply_markup=markup_2)
            friend = resultat[randoms][5]
            break
        elif city in resultat[elem] and id not in resultat[elem]:
            randoms = random.choice(spisok1)
            await update.message.reply_text(f'🎋 Анкеты потенциальных друзей 🎋\n'
                                            f'Имя 🏷: {resultat[randoms][1]} \n'
                                            f'Возраст 🧬: {resultat[randoms][2]} \n'
                                            f'Город 🌆: {resultat[randoms][3]} \n'
                                            f'Хобби 🤿: {resultat[randoms][4]}. \n', reply_markup=markup_2)
            friend = resultat[randoms][5]
            break
    return 'searches'


async def search_second(update, context):
    answer = update.message.text
    if answer == '👍':
        global friend
        await update.message.reply_text(f'Отлично, желаем вам удачи в общении! Вот ваш собеседник:{friend}')
        return ConversationHandler.END
    if answer == '👎':
        await update.message.reply_text('Для просмотра следующей анкеты, отправьте любое сообщение :)!')
        return 'ok'


async def stop():
    pass


async def check_id(update, context):
    id = update.effective_chat.id
    await update.message.reply_text(id)


btn1 = "Регистрация 🧩"
reply_keyboard = [
    ['/anketa', '/help', '/search'],
    ['/registration', '/registration_vk'],
]
reply_keyboard_2 = [['👍',
                     '👎']
                    ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markdown = ReplyKeyboardRemove()
markup_2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=False)
markdown_2 = ReplyKeyboardRemove()


def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('registration', registration)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)],
            5: [MessageHandler(filters.PHOTO & ~filters.COMMAND, fifth_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    vk_handler = ConversationHandler(
        entry_points=[CommandHandler('registration_vk', registration_from_vk)],

        states={
            'vk': [MessageHandler(filters.TEXT & ~filters.COMMAND, vk_id_response)],
            'info_vk': [MessageHandler(filters.TEXT & ~filters.COMMAND, info_vk_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    search_handler = ConversationHandler(
        entry_points=[CommandHandler('search', search)],

        states={
            'searches': [MessageHandler(filters.TEXT & ~filters.COMMAND, search_second)],
            'ok': [MessageHandler(filters.TEXT & ~filters.COMMAND, search)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("anketa", anketa))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("open", open))
    application.add_handler(CommandHandler("check_id", check_id))
    application.add_handler(conv_handler)
    application.add_handler(vk_handler)
    application.add_handler(search_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
