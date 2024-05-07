from roulette.bet_conditions import is_red, is_first_dozen
from roulette.strategy import Martingale, FixedBetStrategy
from roulette.bet_pattern import MultiBetPattern


def main():

    initial_bets = [(is_red, 5)]

    bet_pattern = MultiBetPattern(1000, initial_bets)

    martingale_strategy = Martingale(1000, bet_pattern)

    results = martingale_strategy.bet(10)

    for i, result in enumerate(results, 1):
        print(f"Spin {i}: New Balance={result['new_balance']}, Total Payout={result['total_payout']}")
        for detail in result['details']:
            print(
                f"  {detail['condition']}: Bet Placed={detail['bet_placed']}, Payout={detail['payout']}, Status={detail['status']}")


if __name__ == "__main__":
    main()
