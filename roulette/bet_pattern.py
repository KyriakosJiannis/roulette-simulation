from .bet_conditions import get_payout_multiplier


class BetPattern:
    def __init__(self, bankroll: int):
        if bankroll <= 0:
            raise ValueError("Bankroll must be positive.")
        self.bankroll = bankroll

    def place_bet(self, wheel_outcome: dict) -> dict:
        raise NotImplementedError("Subclass must implement this method.")


class MultiBetPattern(BetPattern):
    def __init__(self, bankroll: int, bets):
        super().__init__(bankroll)
        self.bets = bets

    def place_bet(self, wheel_outcome: dict) -> dict:
        total_payout = 0
        details = []
        for bet_condition, bet_amount in self.bets:
            function_name = bet_condition.__name__ if callable(bet_condition) else bet_condition
            payout_multiplier = get_payout_multiplier(function_name)
            won = bet_condition(wheel_outcome)
            payout = bet_amount * payout_multiplier if won else -bet_amount
            self.bankroll += payout
            total_payout += payout
            details.append({
                'condition': function_name,
                'bet_placed': bet_amount,
                'payout': payout,
                'status': 'Win' if won else 'Loss'
            })
        return {'new_balance': self.bankroll, 'details': details, 'total_payout': total_payout}
