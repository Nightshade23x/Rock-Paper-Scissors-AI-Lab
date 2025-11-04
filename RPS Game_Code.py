from AI_Code import RPS_AI

def game():
    ai=RPS_AI()
    choices=["r","p","s"]
    while True:
        player=input("Enter your choice(r,p or s)")
        computer=ai.choose_ai_move()
    print(f"The computer picked {computer}")
    if player==computer:
        print("It is a draw,duel again!") 
    elif (player=="r" and computer=="s") or \
        (player=="p" and computer=="r") or \
        (player=="s" and computer=="p"):
        print("You beat the system! Congrats")
    else:
        print("You lose,the computer wins!")
    ai.store_moves(player)
if __name__=="__main__":
    game()
    
    