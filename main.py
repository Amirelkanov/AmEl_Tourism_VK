import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from data import Category, VKUserInfo
from data.db_session import global_init, create_session
from extensions.const import SQLALCHEMY_DATABASE_URI, greetings
from extensions.token import VK_BOT_TOKEN
from keyboards.dynamic_keyboards import get_categories_kb, get_articles_kb
from keyboards.static_keyboards import location_keyboard

# Bot init
vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# Launching app
if __name__ == "__main__":

    global_init(SQLALCHEMY_DATABASE_URI)  # Init DB

    # Event loop
    while 1:
        try:
            for event in longpoll.listen():

                if event.type == VkEventType.MESSAGE_NEW and event.to_me:

                    session = create_session()
                    message_text, user_id = event.text, event.user_id
                    location = vk_session.method(
                        "messages.getById", {"message_ids": [event.message_id]}
                    )['items'][0].get("geo", None)

                    user = session.query(VKUserInfo).filter_by(
                        id=user_id).first()

                    if location:

                        user_info = VKUserInfo() if not user else user
                        user_info.id, user_info.page = user_id, 1
                        user_info.coords = \
                            f"{location['coordinates']['latitude']}, " \
                            f"{location['coordinates']['longitude']}"

                        session.add(user_info)
                        session.commit()

                        vk.messages.send(
                            user_id=user_id,
                            message="🌎 Геопозиция получена! С чего начнем?",
                            keyboard=get_categories_kb(session, user_id),
                            random_id=get_random_id()
                        )

                    elif message_text.lower() in greetings:

                        vk.messages.send(
                            user_id=user_id,
                            message="Привет! Я бот, призванный помогать "
                                    "туристам!\n\n"
                                    "Для начала нужно дать доступ к "
                                    "местоположению.",
                            keyboard=location_keyboard(),
                            random_id=get_random_id()
                        )

                    elif message_text in ["«", "»"]:

                        user.page = user.page - 1 if message_text == "«" \
                            else user.page + 1
                        session.add(user)
                        session.commit()

                        vk.messages.send(
                            user_id=user_id,
                            message="Перелистываем...",
                            keyboard=get_categories_kb(session, user_id),
                            random_id=get_random_id()
                        )

                    elif message_text in list(map(lambda x: x.name_of_category,
                                                  session.query(
                                                      Category).all())):

                        kb, articles = get_articles_kb(
                            session, session.query(Category).filter_by(
                                name_of_category=message_text).first().id,
                            user_id)

                        vk.messages.send(
                            user_id=user_id,
                            message=f"Ближайшие {message_text.lower()}:"
                            if articles else "Ничего не найдено 👀",
                            keyboard=kb,
                            random_id=get_random_id()
                        )

        except vk_api.exceptions.ApiError:
            pass
