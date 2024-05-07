import numpy as np
import pandas as pd
import copy
from .bet_pattern import MultiBetPattern
from .strategy import FixedBetStrategy, Martingale


def monte_carlo_simulation(strategy_class, bet_pattern, bankroll, spins, trials):
    """
    Conducts a Monte Carlo simulation and returns the results as a list of ending bankrolls.
    """
    results = []
    for _ in range(trials):
        # Copy bet pattern for each trial to prevent side effects between simulations
        pattern_copy = MultiBetPattern(bankroll, copy.deepcopy(bet_pattern.bets))
        strategy = strategy_class(bankroll, pattern_copy)
        final_results = strategy.bet(spins)
        final_balance = final_results[-1]['new_balance']
        results.append(final_balance)
    return results


def calculate_risk_measures(df):
    """
    Calculates various risk and performance measures for the Monte Carlo simulation results.
    """
    max_drawdown = df['Ending Bankroll'].max() - df['Ending Bankroll'].min()
    volatility = df['Ending Bankroll'].std()
    downside_deviation = df[df['Ending Bankroll'] < df['Initial Bankroll']]['Ending Bankroll'].std()
    average_return = df['Ending Bankroll'].mean()
    median_return = df['Ending Bankroll'].median()
    sharpe_ratio = average_return / volatility if volatility != 0 else np.nan
    sortino_ratio = average_return / downside_deviation if downside_deviation != 0 else np.nan
    probability_of_ruin = (df['Ending Bankroll'] <= 0).mean()
    frequency_large_losses = (df['Ending Bankroll'] < df['Initial Bankroll'] * 0.5).mean()
    value_at_risk_95 = df['Ending Bankroll'].quantile(0.05)
    conditional_value_at_risk_95 = df[df['Ending Bankroll'] < value_at_risk_95]['Ending Bankroll'].mean()

    return {
        'Max Drawdown': max_drawdown,
        'Volatility': volatility,
        'Downside Deviation': downside_deviation,
        'Average Return': average_return,
        'Median Return': median_return,
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Probability of Ruin': probability_of_ruin,
        'Frequency of Large Losses': frequency_large_losses,
        'Value at Risk (95%)': value_at_risk_95,
        'Conditional Value at Risk (95%)': conditional_value_at_risk_95
    }


def run_simulation(bankroll, initial_bet, spins, trials, strategy_class, bet_pattern):
    """
    Runs the Monte Carlo simulation and calculates risk measures.
    """
    ending_balances = monte_carlo_simulation(strategy_class, bet_pattern, bankroll, spins, trials)

    df = pd.DataFrame({
        'Trial Number': range(1, trials + 1),
        'Ending Bankroll': ending_balances,
        'Initial Bankroll': [bankroll] * trials
    })

    risk_measures = calculate_risk_measures(df)
    return df, risk_measures


def main():
    # Set up the bet pattern and strategy
    from .bet_conditions import is_red

    bankroll = 1000
    initial_bet = 50
    spins = 10
    trials = 50
    bet_pattern = MultiBetPattern(bankroll, [(is_red, initial_bet)])

    # Select a strategy
    strategy_class = Martingale

    # Run
    results_df, risk_metrics = run_simulation(bankroll, initial_bet, spins, trials, strategy_class, bet_pattern)
    # Print the results and risk metrics
    print("Risk Metrics:")
    for key, value in risk_metrics.items():
        print(f"{key}: {value}")

    print("\nSample of Simulation Results:")
    print(results_df.head())


if __name__ == "__main__":
    main()
