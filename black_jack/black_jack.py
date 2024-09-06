import random

def deal_card():
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Calculates the score of the current hand of cards."""
    # Check for blackjack (Ace + 10 value card)
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack
    # If the hand contains an Ace (11) and the score is over 21, reduce the Ace to 1
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, dealer_score):
    """Compares user and dealer scores and declares a winner."""
    if user_score == dealer_score:
        return "Draw 🙃"
    elif dealer_score == 0:
        return "Lose, dealer has Blackjack 😱"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif user_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Dealer went over. You win 😁"
    elif user_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"

def play_game():
    print("Welcome to Blackjack!")

    # Initial deal: two cards for user and two for dealer
    user_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]

    game_over = False

    while not game_over:
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(dealer_cards)

        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Dealer's first card: {dealer_cards[0]}")

        # Check if anyone has blackjack
        if user_score == 0 or dealer_score == 0 or user_score > 21:
            game_over = True
        else:
            # Player decides to hit or stand
            user_should_continue = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_continue == 'y':
                user_cards.append(deal_card())
                user_score = calculate_score(user_cards)
            else:
                game_over = True

    # Dealer's turn: dealer must draw until they reach a score of 17 or more
    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)

    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Dealer's final hand: {dealer_cards}, final score: {dealer_score}")
    print(compare(user_score, dealer_score))

# Main game loop
while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == 'y':
    play_game()
