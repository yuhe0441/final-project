# main.py - Game entry point
# Run this file to start the game

from game import DetectiveGame

def main():
    print("  :)Welcome to Detective Mystery Game ！ ")
    print("Solve the crime before your moves run out!\n")
    
    difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
    game = DetectiveGame(difficulty)
    game.start_game()

if __name__ == "__main__":
    main()
