# Agents Gizathon: Mitchi - ETH Leverage Vault

The project deploys an ERC4626 vault on Starknet that leverages and deleverages ETH positions based on predictions by a verifiable ML model.
For vault strategist: They don't have to reveal their model and strategy to the public but still be able to attract investments from users based on their onchain performance.
For users: They can see the historical performance of the vault before investing and trust the performance of the model rather than subjectivity of the strategist.

## Overview

- `model/`: Contains the code for the data, features and the training of the model
- `model/experiments`: Contains Jupyter notebooks for iterations of the model
- `vault/`: Contains Cairo code for Vault ERC4626
- `create_agent.py`: Creates a Giza agent - since the giza cli doesn't work
- `agent.py`: Code for taking the latest data and generating a prediction. Based on the prediction calls the `rebalance` function on the contract. This code is not functional as Giza's support for starknet doesn't work.

## Improvements

- [ ] Add more features to the model to increase the accuracy from 64% to 75%
- [ ] Instead of gating rebalance on the wallet address, verify the proof on chain before executing
- [ ] Integrate with Nostra, zkLend or ZKX on mainnet to leverage and deleverage positions
