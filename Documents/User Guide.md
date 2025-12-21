This program allows the user to play the classic game of Rock Paper Scissors against an AI that uses a Markov chain system to predict your moves. Below are the instructions on how to begin.

**How to run the program**

1.Ensure all project files are downloaded including RPS_Game_Code.py and ai_code.py.

2.Navigate to the Main Game folder and open RPS_Game_Code.py

3.Run the file

**How to play**

During the run, you will be asked to repeatedly enter your move.

Valid inputs are r,p,s or q. r stands for rock, p for paper and s for scissors.

q is to quit and view win loss stats and the best performing model in the last 5 rounds.

Note, input is case insensitive, so upper or lowercase is valid. Any other input will result in text of "Invalid choice, try again"

**Game Flow:**

After each round, the AI will predict your next move and play it against you. The program will track your wins and losses, along with ties and the performance of each model in the last 5 rounds.

**How to read model statistics:**

Each win gives the model a +1,a loss gives -1 and a draw gives 0. When the game is quit, the score arrays printed in the terminal represent each model's performance over the last five rounds.

**Ending the game:**

As mentioned above, simply pressing q ends the game.

