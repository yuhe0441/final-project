# game.py - Core game logic

from locations import locations
from suspects import suspects
import random

class DetectiveGame:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.set_difficulty()
        self.culprit = random.choice(list(suspects.keys()))
        self.discovered_clues = []
        self.visited_locations = []
        self.game_over = False
        
    def set_difficulty(self):
        if self.difficulty == "easy":
            self.moves_left = 15
            self.red_herring_ratio = 0.2
        elif self.difficulty == "hard":
            self.moves_left = 8
            self.red_herring_ratio = 0.5
        else:  # medium
            self.moves_left = 10
            self.red_herring_ratio = 0.3
    
    def start_game(self):
        print(f"\nCase Started: The Murder at Blackwood Manor")
        print(f"Difficulty: {self.difficulty.capitalize()}")
        print(f"Initial moves: {self.moves_left}\n")
        
        while not self.game_over and self.moves_left > 0:
            self.display_status()
            self.player_turn()
        
        if self.game_over:
            return
        print("\nCase Closed Unsolved - The killer escaped!")
    
    def display_status(self):
        print(f"\nMoves left: {self.moves_left}")
        print("Discovered clues:", ", ".join(self.discovered_clues) if self.discovered_clues else "None")
    
    def player_turn(self):
        action = input("\nChoose action:\n1. Explore location\n2. Interview suspect\n3. Make accusation\n> ")
        
        if action == "1":
            self.explore_location()
        elif action == "2":
            self.interview_suspect()
        elif action == "3":
            self.make_accusation()
        else:
            print("Invalid choice")
    
    def explore_location(self):
        print("\nAvailable locations:")
        for i, loc in enumerate(locations.keys(), 1):
            print(f"{i}. {loc}")
        
        choice = input("Choose location number: ")
        try:
            location = list(locations.keys())[int(choice)-1]
        except (ValueError, IndexError):
            print("Invalid location choice")
            return
        
        self.visited_locations.append(location)
        clues = locations[location]
        
        # Determine if clue is relevant or red herring
        if random.random() < self.red_herring_ratio and len(clues["red_herrings"]) > 0:
            clue = random.choice(clues["red_herrings"])
            print(f"\nFound: {clue} (This might not be important)")
        else:
            clue = random.choice(clues["relevant"])
            print(f"\nFound: {clue}")
            self.discovered_clues.append(clue)
        
        self.moves_left -= 1
    
    def interview_suspect(self):
        print("\nSuspects available:")
        for i, suspect in enumerate(suspects.keys(), 1):
            print(f"{i}. {suspect.capitalize()}")
        
        choice = input("Choose suspect number: ")
        try:
            suspect = list(suspects.keys())[int(choice)-1]
        except (ValueError, IndexError):
            print("Invalid suspect choice")
            return
        
        print(f"\nInterviewing {suspect.capitalize()}:")
        print(f"Alibi: {suspects[suspect]['alibi']}")
        print(f"Motive: {suspects[suspect]['motive']}")
        
        if random.random() < 0.3:  # 30% chance to discover secret
            print(f"Secret: {suspects[suspect]['secret']}")
        
        self.moves_left -= 1
    
    def make_accusation(self):
        print("\nMake your accusation:")
        for i, suspect in enumerate(suspects.keys(), 1):
            print(f"{i}. {suspect.capitalize()}")
        
        suspect_choice = input("Choose suspect number: ")
        try:
            accused = list(suspects.keys())[int(suspect_choice)-1]
        except (ValueError, IndexError):
            print("Invalid suspect choice")
            return
        
        print("\nSelect 2 key clues to support your accusation:")
        for i, clue in enumerate(self.discovered_clues, 1):
            print(f"{i}. {clue}")
        
        try:
            clue_indices = input("Enter two clue numbers separated by space: ").split()
            clue1 = self.discovered_clues[int(clue_indices[0])-1]
            clue2 = self.discovered_clues[int(clue_indices[1])-1]
        except (ValueError, IndexError):
            print("Invalid clue selection")
            return
        
        if accused == self.culprit and self.check_winning_clues(clue1, clue2):
            print(f"\n:) You convicted the {accused} with {clue1} and {clue2}!")
            print("Case Solved! Congratulations Detective!")
        else:
            print("\nWrong accusation! The real killer escapes...")
            print(f"The real culprit was {self.culprit}!")
        
        self.game_over = True
    
    def check_winning_clues(self, clue1, clue2):
        # Simple check 
        winning_pairs = [
            ("bloody knife", "torn clothing"),
            ("poison vial", "ledger"),
            ("handwritten note", "diary")
        ]
        return (clue1.lower(), clue2.lower()) in winning_pairs
