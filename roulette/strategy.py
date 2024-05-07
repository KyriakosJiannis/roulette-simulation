from .roulette import RouletteWheel
from .bet_pattern import BetPattern, MultiBetPattern
import copy


class FixedBetStrategy:
    def __init__(self, bankroll: int, bet_pattern: BetPattern):
        self.bankroll = bankroll
        self.bet_pattern = bet_pattern
        self.wheel = RouletteWheel()

    def spin_wheel(self):
        return self.wheel.spin()

    def update_bankroll(self, result: dict):
        self.bankroll = result['new_balance']

    def bet(self, spins: int) -> list:
        results = []
        for spin in range(1, spins + 1):
            if self.bankroll <= 0:
                print("Stopping early: Bankroll depleted.")
                break
            total_bet = sum(amount for _, amount in self.bet_pattern.bets)
            if total_bet > self.bankroll:
                print(f"Cannot place bets totaling ${total_bet} with bankroll of ${self.bankroll}.")
                break
            outcome = self.spin_wheel()
            result = self.bet_pattern.place_bet(outcome)
            self.update_bankroll(result)
            results.append(result)
        return results


class Martingale(FixedBetStrategy):
    def __init__(self, bankroll: int, bet_pattern: BetPattern):
        super().__init__(bankroll, bet_pattern)
        self.original_bets = copy.deepcopy(bet_pattern.bets)
        self.current_bets = copy.deepcopy(bet_pattern.bets)

    def update_bet(self, result):
        all_losses = all(detail['status'] == "Loss" for detail in result['details'])

        if all_losses:
            # Double each bet if all conditions resulted in a loss
            self.current_bets = [(condition, min(2 * amount, self.bankroll))
                                 for condition, amount in self.current_bets]
        else:
            # Reset to original bets if any condition results in a win
            self.current_bets = copy.deepcopy(self.original_bets)

        self.bet_pattern.bets = copy.deepcopy(self.current_bets)

    def bet(self, spins: int) -> list:
        results = []
        for spin in range(1, spins + 1):
            if self.bankroll <= 0:
                #print("Bankroll depleted. Stopping early.")
                break
            total_bet = sum(amount for _, amount in self.current_bets)
            if total_bet > self.bankroll:
                #print(f"Adjusted bet to bankroll limit. Original bet was ${total_bet}.")
                self.adjust_bets_to_bankroll()
            outcome = self.spin_wheel()
            result = self.bet_pattern.place_bet(outcome)
            self.update_bankroll(result)
            self.update_bet(result)
            results.append(result)
            # print(f"Result after spin {spin}: New balance: {result['new_balance']}, Payout: {result['total_payout']}")
        return results

    def adjust_bets_to_bankroll(self):
        # Adjust bets to not exceed the bankroll
        scale_factor = self.bankroll / sum(amount for _, amount in self.current_bets)
        self.current_bets = [(condition, int(amount * scale_factor)) for condition, amount in self.current_bets]
        self.bet_pattern.bets = copy.deepcopy(self.current_bets)



