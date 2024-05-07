"""
Bet Condition Functions for Roulette Simulation

This script defines a set of functions that determine the outcome of various bet conditions in a roulette game.
Each function takes a dictionary representing the outcome of a roulette wheel spin and returns a boolean indicating
whether the bet condition has been met. The script also includes a function to retrieve the payout multiplier for
each bet condition.
"""


def is_red(wheel_outcome):
    return wheel_outcome['color'] == 'red'


def is_black(wheel_outcome):
    return wheel_outcome['color'] == 'black'


def is_even(wheel_outcome):
    return wheel_outcome['number'] % 2 == 0 and wheel_outcome['number'] != 0


def is_odd(wheel_outcome):
    return wheel_outcome['number'] % 2 != 0


def is_low(wheel_outcome):
    return 1 <= wheel_outcome['number'] <= 18


def is_high(wheel_outcome):
    return 19 <= wheel_outcome['number'] <= 36


def is_first_dozen(wheel_outcome):
    return 1 <= wheel_outcome['number'] <= 12


def is_second_dozen(wheel_outcome):
    return 13 <= wheel_outcome['number'] <= 24


def is_third_dozen(wheel_outcome):
    return 25 <= wheel_outcome['number'] <= 36


def is_column(wheel_outcome, column_number):
    return wheel_outcome['column'] == column_number


def is_single_number(wheel_outcome, number):
    return wheel_outcome['number'] == number


def is_section(wheel_outcome, section_name):
    return wheel_outcome['section'] == section_name


def get_payout_multiplier(condition_name):
    condition_to_payout = {
        'is_red': 1,
        'is_black': 1,
        'is_even': 1,
        'is_odd': 1,
        'is_low': 1,
        'is_high': 1,
        'is_first_dozen': 2,
        'is_second_dozen': 2,
        'is_third_dozen': 2,
        'is_column': 2,
        'is_single_number': 35
    }
    return condition_to_payout.get(condition_name, 1)
