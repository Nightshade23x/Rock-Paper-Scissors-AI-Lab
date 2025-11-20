from ai_code import Multi_RPS_AI

def game():
    ai = Multi_RPS_AI()
    choices = ["r", "p", "s", "q"]
    player_history = []

    while True:
        player = input("Enter your choice (r, p, s) or q for stats: ").lower()

        # Hnaldes quit option and shows stats of each model in the last 5 games.
        if player == "q":
            print("\nAI Model Statistics")
            for i, s in enumerate(ai.scores, start=1):
                print(f"Memory {i}: {s}   sum = {sum(s)}")
            print(f"→ Best model: memory_length = {ai.best_ai().memory_length}")
            continue

        # handles invalid input
        if player not in ["r", "p", "s"]:
            print("Invalid choice, try again.")
            continue

        # Saves move
        player_history.append(player)

        # picks the best ai move to counter the player
        computer = ai.get_move()
        print(f"The computer picked {computer}")

        # Determine the result of the game
        if player == computer:
            print("It is a draw.")
        elif (player == "r" and computer == "s") or \
             (player == "p" and computer == "r") or \
             (player == "s" and computer == "p"):
            print("You beat the system! Congrats!")
        else:
            print("You lose, the computer wins!")

        # Updating of models happens here
        ai.update_all(player)
        ai.update_scores(player) 


if __name__ == "__main__":
    game()
