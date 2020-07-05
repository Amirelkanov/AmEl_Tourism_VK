#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Finding the distance between two points """

from math import radians, cos, sqrt


def lonlat_distance(first_coords: list, second_coords: list) -> float:
    """
    :param first_coords: first GPS - coordinates
    :param second_coords: second GPS - coordinates
    :return: distance between two gps points (in km)
    """

    first_lon, first_lat = first_coords
    second_lon, second_lat = second_coords

    radians_latitude = radians((first_lat + second_lat) / 2.)
    lat_lon_factor = cos(radians_latitude)

    dx, dy = abs(first_lon - second_lon) * 111. * lat_lon_factor, abs(
        first_lat - second_lat) * 111.
    distance = sqrt(dx * dx + dy * dy)

    return distance
