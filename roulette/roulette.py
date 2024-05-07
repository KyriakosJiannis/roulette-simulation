import random


class RouletteWheel:
    _red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    _black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33}
    _green_numbers = {0}

    _voisins = {22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25}
    _tiers = {27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33}
    _orphelins = {1, 20, 14, 31, 9, 6, 34, 17}

    def __init__(self):
        self.numbers = list(range(0, 37))  # 0-36

    def spin(self):
        result = random.choice(self.numbers)
        return {
            'number': result,
            'color': self.get_color(result),
            'is_even': result % 2 == 0 if result != 0 else None,
            'is_low': 1 <= result <= 18,
            'is_high': 19 <= result <= 36,
            'dozen': self.determine_dozen(result),
            'column': self.determine_column(result),
            'section': self.determine_section(result)
        }

    @staticmethod
    def get_color(number):
        if number in RouletteWheel._red_numbers:
            return 'red'
        elif number in RouletteWheel._black_numbers:
            return 'black'
        elif number in RouletteWheel._green_numbers:
            return 'green'
        return None

    @staticmethod
    def determine_dozen(number):
        if 1 <= number <= 12:
            return 1
        elif 13 <= number <= 24:
            return 2
        elif 25 <= number <= 36:
            return 3
        return None

    @staticmethod
    def determine_column(number):
        if number % 3 == 1:
            return 1
        elif number % 3 == 2:
            return 2
        elif number % 3 == 0 and number != 0:
            return 3
        return None

    def determine_section(self, number):
        if number in RouletteWheel._voisins:
            return 'voisins'
        elif number in RouletteWheel._tiers:
            return 'tiers'
        elif number in RouletteWheel._orphelins:
            return 'orphelins'
        return None

    @property
    def red_numbers(self):
        return self._red_numbers


def main():
    wheel = RouletteWheel()
    print("Testing 10 spins of the roulette wheel:")
    for _ in range(10):
        result = wheel.spin()
        print(f"Spin result: Number={result['number']}, Color={result['color']}, "
              f"Is Even={result['is_even']}, Is Low={result['is_low']}, Is High={result['is_high']}, "
              f"Dozen={result['dozen']}, Column={result['column']}, Section={result['section']}")


if __name__ == "__main__":
    main()

