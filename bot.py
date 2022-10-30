import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
START, GENDER, AGE, PHOTO, VIDEO, LOCATION, WAYF, FAMILY, MUSIC, HOBBI, BIO = range(
    11)


def hi_command(update, _):
    update.message.reply_text(f'Hi, {update.effective_user.first_name}! \n'
                              'Пожалуйста, поздоровайся со мной, мне будет приятно. \n'
                              'Или введи /cancel, чтобы прекратить разговор.\n\n')
    return START


def start(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s поздоровался: %s",
                user.first_name, update.message.text)
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Если ты непротив, я проведу небольшой опрос, чтобы узнать тебя получше. '
        'Ты мальчик или девочка?',
        reply_markup=markup_key,)
    return GENDER

# Обрабатываем пол пользователя


def gender(update, _):
    user = update.message.from_user
    logger.info("Пол %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Хорошо. Сколько тебе лет, если не секрет? Если считаешь, что о возрасте спрашивать неприлично, отправь /skip.',
        reply_markup=ReplyKeyboardRemove(),)
    return AGE


def age(update, _):
    user = update.message.from_user
    logger.info("Возраст %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Да у тебя еще вся жизнь впереди! Пришли мне свою фотографию, чтоб я знал как ты '
        'выглядишь, или отправь /skip, если стесняешься.')
    return PHOTO


def skip_age(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не указал возраст.", user.first_name)
    update.message.reply_text(
        'Нет, так нет, пусть это останется тайной! Пришли мне свою фотографию, чтоб я знал как ты '
        'выглядишь, или отправь /skip, если стесняешься.')
    return PHOTO


def photo(update, _):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'{user.first_name}_photo.jpg')
    logger.info("Фотография %s: %s", user.first_name,
                f'{user.first_name}_photo.jpg')
    update.message.reply_text(
        'Великолепно! А как насчет видеоприветствия? Или отправь /skip,  если нет вдохновения.')
    return VIDEO


def skip_photo(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не отправил фото.", user.first_name)
    update.message.reply_text(
        'Держу пари, ты выглядишь великолепно! А как насчет видеоприветствия? '
        'Или отправь /skip, если совсем не хочешь показывать себя.'
    )
    return VIDEO


def video(update, _):
    user = update.message.from_user
    video_file = update.message.video.get_file()
    video_file.download(f'{user.first_name}_video.mp4')
    logger.info("Видео %s: %s", user.first_name,
                f'{user.first_name}_video.mp4')
    update.message.reply_text(
        'Отлично держишься в кадре! А теперь пришли мне свое'
        ' местоположение, или /skip если параноик.')
    return LOCATION


def skip_video(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не отправил видео.", user.first_name)
    update.message.reply_text(
        'Видимо, ты не любишь камеру...или она тебя) А теперь пришлите мне'
        ' свое местоположение, или /skip если параноик.')
    return LOCATION


def location(update, _):
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Местоположение %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text(
        'Может быть, я смогу как-нибудь навестить тебя!'
        'Расскажи о своей семье, или /skip, если это личное дело')
    return FAMILY


def skip_location(update, _):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'Видимо параноик! Ну может скажешь откуда ты, хотя бы примерно, откуда ты?...или все_таки параноик, тогда /skip'
    )
    return WAYF


def wh_a_y_from(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s живет в %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Может быть, я смогу как-нибудь навестить тебя! '
        'Расскажи о своей семье, или /skip, если это личное дело')
    return FAMILY


def skip_wh_a_y_from(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не рассказал о месте жительства.",
                user.first_name)
    update.message.reply_text(
        'Точно параноик! Ладно, тогда расскажи о своей семье, или /skip, если это личное дело')
    return FAMILY


def family(update, _):
    user = update.message.from_user
    logger.info("Семья пользователя %s: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Прекрасно! '
        'Давай поговорим об увлечениях? Тебе нравится музыка? Пришли свою любимую песню или /skip, если любишь тишину')
    return MUSIC


def skip_family(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не рассказал о своей семье.", user.first_name)
    update.message.reply_text(
        'Дело твое. '
        'Давай поговорим об увлечениях? Тебе нравится музыка? Пришли свою любимую песню или /skip, если любишь тишину')
    return MUSIC


def music(update, _):
    user = update.message.from_user
    audio_file = update.message.audio.get_file()
    audio_file.download(f'{user.first_name}_audio.mp3')
    logger.info("Трек %s: %s", user.first_name, f'{user.first_name}_audio.mp3')
    update.message.reply_text(
        'Отличный вкус! А какое у тебя хобби? Или отправь /skip,  если его нет.')
    return HOBBI


def skip_music(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не отправил запись.", user.first_name)
    update.message.reply_text(
        'Видимо слишком большой выбор, ведь все любят музыку! А как насчет хобби? Или отправь /skip, если его нет.')
    return HOBBI


def hobbi(update, _):
    user = update.message.from_user
    logger.info("Хобби пользователя %s: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Какая ты разносторонняя личность! '
        'Может хочешь рассказать о чем-то еще? Или /skip, если и так достаточно')
    return BIO


def skip_hobbi(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не рассказал о своих хобби.", user.first_name)
    update.message.reply_text(
        'Надеюсь, ты найдешь что-то свое. '
        'Может расскажешь хоть о чем-нибудь? Или /skip, если неохота')
    return BIO


def bio(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s рассказал: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Спасибо! Надеюсь, когда-нибудь снова сможем поговорить. '
        f'До скорых встреч, {update.effective_user.first_name}!')
    return ConversationHandler.END


def skip_bio(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s ничего не рассказал", user.first_name)
    update.message.reply_text(
        'Что же, надеюсь, когда-нибудь мы сможем поговорить по душам. '
        f'До скорых встреч, {update.effective_user.first_name}!')
    return ConversationHandler.END

# Обрабатываем команду /cancel если пользователь отменил разговор


def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("TOKEN")
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler`
    conv_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', hi_command)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            START: [MessageHandler(Filters.text & ~Filters.command, start)],
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age), CommandHandler('skip', skip_age)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            VIDEO: [MessageHandler(Filters.video, video), CommandHandler('skip', skip_video)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            WAYF: [MessageHandler(Filters.text & ~Filters.command, wh_a_y_from), CommandHandler('skip', skip_wh_a_y_from)],
            FAMILY: [MessageHandler(Filters.text & ~Filters.command, family), CommandHandler('skip', skip_family)],
            MUSIC: [MessageHandler(Filters.text & ~Filters.command, music), CommandHandler('skip', skip_music)],
            HOBBI: [MessageHandler(Filters.text & ~Filters.command, hobbi), CommandHandler('skip', skip_hobbi)],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio), CommandHandler('skip', skip_bio)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()