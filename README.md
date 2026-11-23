# Rock–Paper–Scissors AI Lab

A Python experiment in adaptive game AI: a Rock–Paper–Scissors opponent learns from move histories and tries to predict the next human move instead of always choosing at random.

## Approach

- Uses Markov-chain/prefix-history predictions from previous moves.
- Explores multiple context lengths (up to five previous moves) and selecting between predictors based on recent performance.
- Chooses the counter to its predicted human move and falls back to random selection when there is insufficient history.
- Saves move information in JSON files so experiments can reuse history.
- Includes unit/integration testing and coursework reports.

## Repository layout

- `Main Game/` — Python game and AI implementation, including the prediction and move-storage modules.
- `Testing/` — test code.
- `Documents/`, `Weekly Reports/` — project documentation and progress reports.
- `moves.json`, `tests_single.json`, `integration_test.json` — stored game/test data.
- `Coverage Report.png` — test-coverage artifact.

## Run locally

Requires Python 3. Clone the repository, then run the game script in `Main Game/` (the repository has used `rps_game.py` / `RPS Game_Code.py` for its gameplay entry point).

```powershell
git clone https://github.com/Nightshade23x/Rock-Paper-Scissors-AI-Lab.git
cd Rock-Paper-Scissors-AI-Lab
```

Use the actual game entry-point filename present in `Main Game/` when running it. Core prediction and storage logic uses Python's standard library; coverage measurement uses the optional `coverage` package.

## Testing

The repository includes tests for prediction logic, stored transition histories and game integration. From the repository root, a typical discovery command is:

```powershell
python -m unittest discover -s Testing
```

## Project context

This is a learning and experimentation project. Prediction accuracy depends on the opponent's behavior and the available move history; it does not guarantee wins against random play.
