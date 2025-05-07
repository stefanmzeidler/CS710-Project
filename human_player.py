from player import Player

class HumanPlayer(Player):
    def __init__(self, name="You"):
        super().__init__(name)

    def choose_card(self, game_state):
        print(f"\n{self.name}'s Turn — Turn {game_state['turn'][0] + 1}")
        print("Your hand:")
        for index, card in enumerate(self.hand):
            print(f"{index}: {card}")

        while True:
            try:
                choice = int(input("Enter the number of the card you want to play: "))
                if 0 <= choice < len(self.hand):
                    return self.hand[choice]
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a number.")
