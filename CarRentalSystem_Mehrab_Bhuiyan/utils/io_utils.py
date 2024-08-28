def get_input(prompt, required=True, input_type=str):
    """
    Function to get input from the user.
    :param prompt: The prompt to show the user.
    :param required: Whether the input is required.
    :param input_type: The type to cast the input to (e.g., str, int, float).
    :return: The user's input, cast to the correct type.
    """
    while True:
        user_input = input(prompt)
        if not user_input and required:
            print("This field is required. Please enter a value.")
            continue
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")
            continue

def display_message(message):
    """
    Function to display a message to the user.
    :param message: The message to display.
    """
    print(message)

def get_password(prompt="Enter your password: "):
    """
    Function to securely get a password input from the user.
    :param prompt: The prompt to show the user.
    :return: The user's password input.
    """
    from getpass import getpass
    return getpass(prompt)

def confirm_action(prompt="Are you sure? (y/n): "):
    """
    Function to confirm an action with the user.
    :param prompt: The confirmation prompt to show the user.
    :return: True if the user confirms, False otherwise.
    """
    while True:
        confirmation = input(prompt).lower()
        if confirmation in ['y', 'yes']:
            return True
        elif confirmation in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")
