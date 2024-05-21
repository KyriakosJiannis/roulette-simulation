import streamlit as st
import pandas as pd
import plotly.express as px
import copy
from roulette.bet_pattern import MultiBetPattern
from roulette.strategy import FixedBetStrategy, Martingale
from roulette.bet_conditions import (is_red, is_black, is_even, is_odd, is_low, is_high,
                                     is_first_dozen, is_second_dozen, is_third_dozen)
from roulette.simulation import run_simulation

st.title('Roulette Strategy Tester')
st.write("""
This application allows you to test different roulette betting strategies through simulations with customizable bet patterns.
Select your bet conditions, set your parameters, and run the simulation to see the outcomes and risk measures visualized below.
""")

# Define a dictionary to map bet conditions to functions
bet_conditions = {
    'Red': is_red, 'Black': is_black, 'Even': is_even, 'Odd': is_odd,
    'Low': is_low, 'High': is_high, 'First Dozen': is_first_dozen,
    'Second Dozen': is_second_dozen, 'Third Dozen': is_third_dozen
}

# Initialize session state for storing bets
if 'bets' not in st.session_state:
    st.session_state.bets = []


# Function to add a bet to the list
def add_bet():
    bet_condition = st.session_state['bet_choice']
    bet_amount = st.session_state['bet_amount']
    if bet_amount > 0:
        st.session_state.bets.append((bet_conditions[bet_condition], bet_amount))
        st.success(f"Added bet on {bet_condition} with amount ${bet_amount}")


# User inputs for adding bets
bet_choice = st.selectbox('Choose your bet condition:', list(bet_conditions.keys()), key='bet_choice')
bet_amount = st.number_input('Bet Amount:', min_value=0.5, value=5, format='%d', key='bet_amount')
st.button('Add Bet', on_click=add_bet)

# Display current bets
st.write("### Current Bets")
for i, (func, amount) in enumerate(st.session_state.bets, 1):
    st.write(f"{i}. {func.__name__}: ${amount}")

# Simulation parameters
strategy_choice = st.radio('Choose your betting strategy:', ('Fixed Bet Strategy', 'Martingale'))
bankroll = st.number_input('Initial bankroll:', min_value=100, value=1000, format='%d')
spins = st.slider('Number of spins:', 10, 500, 100)
trials = st.slider('Number of trials:', 10, 1000, 100)

# Simulation button
if st.button('Run Simulation') and st.session_state.bets:
    total_bet = sum(amount for _, amount in st.session_state.bets)
    if total_bet > bankroll:
        st.error(f"Total bet amount ${total_bet} exceeds your bankroll of ${bankroll}. Please adjust your bets.")
    else:
        bet_pattern = MultiBetPattern(bankroll, copy.deepcopy(st.session_state.bets))
        strategy_class = FixedBetStrategy if strategy_choice == 'Fixed Bet Strategy' else Martingale
        results_df, risk_metrics = run_simulation(bankroll, 100, spins, trials, strategy_class, bet_pattern)

    # Plot results
    fig = px.line(results_df, x='Trial Number', y='Ending Bankroll', title='Ending Bankroll Per Trial')
    st.plotly_chart(fig, use_container_width=True)
    hist_fig = px.histogram(results_df, x='Ending Bankroll', nbins=30, title='Distribution of Ending Bankrolls')
    st.plotly_chart(hist_fig, use_container_width=True)
    st.write("### Risk Measures")
    risk_df = pd.DataFrame.from_dict(risk_metrics, orient='index', columns=['Value'])
    st.table(risk_df)

# Clear bets button
if st.button('Clear Bets'):
    st.session_state.bets = []
    st.experimental_rerun()
