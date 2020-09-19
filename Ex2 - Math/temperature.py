# FILE : temperature.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019


def is_it_summer_yet(min_temp, temp_day1, temp_day2, temp_day3):
    """ Checks if the temperature in the given 3 days
     is higher then the minimum for at least 2 days
    :param min_temp: the lowest required temperature
    :param temp_day1: first day temperature
    :param temp_day2: second day temperature
    :param temp_day3: third day temperature
    :return: true if the temperature was higher then the minimum
    for at least 2 days, false otherwise
    :rtype: boolean
    """
    # Checks if each day's temperature is above the required minimum
    is_day1_hotter = temp_day1 > min_temp
    is_day2_hotter = temp_day2 > min_temp
    is_day3_hotter = temp_day3 > min_temp
    # Checks whether there is 2 days above minimum temperature or not
    if is_day1_hotter and (is_day2_hotter or is_day3_hotter):
        return True
    if is_day2_hotter and is_day3_hotter:
        return True
    return False
