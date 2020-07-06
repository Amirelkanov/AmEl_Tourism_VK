#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import ceil

from vk_api.keyboard import VkKeyboard

from data import VKUserInfo, Article, Category
from extensions.const import max_num_of_categories_per_page
from extensions.formatting_distance import lonlat_distance


def get_articles_kb(session, category_id: int, user_id: int):
    """
    :param session: SQLAlchemy session object
    :param category_id: id of the category by which articles will be searched
    :param user_id: id of current user
    :return: inline category keyboard and name of category
    """

    keyboard = VkKeyboard(inline=True)

    # Formatting the user coords
    coords = list(map(float, session.query(VKUserInfo).filter_by(
        id=user_id).first().coords.split(", ")))

    # Sorting places by proximity to the user
    articles = sorted(session.query(Article).filter_by(
        article_category_id=category_id).all(),
                      key=lambda x: lonlat_distance(coords, list(
                          map(float, x.coords.split(", ")))), reverse=True)[:5]

    # Adding articles
    for i, article in enumerate(articles):

        # keyboard.add_openlink_button(f"{article.title}",
        #                              link=f"{article_url}/{article.id}")
        # Пока сайт не будет размещен на платном хостинге,
        # данная строчка будет закомментирована

        keyboard.add_openlink_button(f"{article.title}",
                                     link="https://wikipedia.org/")

        if i + 1 != len(articles):
            keyboard.add_line()

    return keyboard.get_keyboard(), articles


def get_categories_kb(session, user_id: int):
    """
    :param session: SQLAlchemy session object
    :param user_id: id of current user
    :return: inline category keyboard
    """

    keyboard = VkKeyboard()

    # Adding categories
    categories = session.query(Category).all()
    page = session.query(VKUserInfo).filter_by(id=user_id).first().page

    for category in categories[max_num_of_categories_per_page * (
            page - 1):max_num_of_categories_per_page * page]:
        keyboard.add_button(category.name_of_category)
        keyboard.add_line()

    # Adding nav arrows
    if page > 1:
        keyboard.add_button("«")
    if ceil(len(categories) / max_num_of_categories_per_page) > page:
        keyboard.add_button("»")

    # Adding location button
    keyboard.add_line()
    keyboard.add_location_button()

    return keyboard.get_keyboard()
