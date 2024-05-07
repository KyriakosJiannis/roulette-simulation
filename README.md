# Roulette Simulation

## Overview
Roulette Simulation enables Monte Carlo simulations of diverse betting strategies in roulette. 
It offers functionality for simulating different strategies, computing risk measures, 
running simulations with customizable parameters, 
and visualizing the results through a Streamlit application.

## Installation

To get started with this project, clone the repository.

```bash
git clone https://github.com/KyriakosJiannis/roulette-simulation.git
cd roulette-simulation
```

## Usage
To run the Streamlit application in local machine.
```bash
streamlit run streamlit_app.py
```

Alternative running the Docker Container

Build the Docker Image
```bash
docker build -t roulette-simulation .
```
Run the Docker Container
```bash
docker run -p 8501:8501 roulette-simulation
```

open the browser at http://localhost:8501


## Betting Strategies

The project offers a variety of betting strategies which users can apply in simulations, each with its own unique approach:

- **FixedBetStrategy**: Maintains a constant bet amount regardless of previous outcomes.
- **Martingale**: Doubles the bet after each loss, aiming to recover losses from previous rounds with a single win.

users can define custom strategies based on the outcome properties, utilizing the following bet conditions:

- **Red/Black**: Bet based on the color outcome of the spin.
- **Even/Odd**: Bet on whether the outcome number will be even or odd.
- **Low/High**: Bet on whether the number will be in the low range (1-18) or high range (19-36).
- **Dozens**: Choose from three dozen ranges:
- **First Dozen** (1-12)
- **Second Dozen** (13-24)
- **Third Dozen** (25-36)



## Features

Choose between different betting strategies and set  parameters like bankroll, bet size, number of spins, 
and trials for Monte Carlo simulation. Visualize simulation results with dynamic graphs using Plotly.

Set the inputs parameters
<img src="/pictures/inputs.png" width="600"  alt="inputs">

Finalise the simulation
<img src="/pictures/setup.png" width="600"  alt="inputs">

Run the simulation and get the output
<img src="/pictures/distributions.png" width="600"  alt="inputs">

<img src="/pictures/Risk measurements.png" width="600"  alt="inputs">


## License

Completely free and open-source and licensed under the MIT license