# utilities.py - Utility helper functions

def display_title():
    title = """
    DETECTIVE MYSTERY GAME!

    """
    print(title)

def validate_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(options)}")
