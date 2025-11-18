from ai_code import Multi_RPS_AI

def game():
    ai=Multi_RPS_AI()
    choices=["r","p","s"]
    player_history=[]

    while True:
        player=input("Enter your choice(r,p or s)").lower()
        if player not in choices:
            print("Please try again")
            continue
        player_history.append(player)
        computer=ai.get_move(player_history)
        print(f"The computer picked {computer}")

        if player==computer:
            result=0
            print("It is a draw,duel again!")

        elif (player=="r" and computer=="s") or \
            (player=="p" and computer=="r") or \
            (player=="s" and computer=="p"):
            result=-1
            print("You beat the system! Congrats")

        else:
            result=1
            print("You lose,the computer wins!")

        ai.update_all(player)
        ai.update_scores(result)

if __name__=="__main__":
    game()

