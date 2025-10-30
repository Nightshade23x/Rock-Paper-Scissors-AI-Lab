import random
def game():
    choices=["r","p","s"]
    player=input("Enter your choice(R,P or S)")
    computer=random.choice(choices)
    print(f"The computer picked {computer}")
    if player==computer:
        print("It is a draw,duel again!") 
    elif (player=="r" and computer=="s") or \
        (player=="p" and computer=="r") or \
        (player=="s" and computer=="p"):
        print("You win")
    else:
        print("You lose,the computer wins!")
if __name__=="__main__":
    game()
    
    