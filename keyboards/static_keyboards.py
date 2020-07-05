#!/usr/bin/python
# -*- coding: utf-8 -*-

from vk_api.keyboard import VkKeyboard


def location_keyboard():
    """
    :return: keyboard which prompts for the location
    """

    keyboard = VkKeyboard()
    keyboard.add_location_button()

    return keyboard.get_keyboard()
