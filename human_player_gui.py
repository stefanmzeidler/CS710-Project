from player import Player
import copy

class HumanPlayerGUI(Player):
    def __init__(self, name="You", ui=None):
        super().__init__(name)
        self.ui = ui


    def __getstate__(self):
        state = self.__dict__.copy()
        state['ui'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.ui = None


    def choose_card(self, game_state):
        self.ui.card_choice = None

        def select_card(card):
            self.ui.card_choice = card

        self.ui.update_hand(self.hand, select_card)

        # Poll for card selection
        while self.ui.card_choice is None:
            self.ui.root.update_idletasks()
            self.ui.root.update()

        return self.ui.card_choice

    def clone(self):
        player_copy = HumanPlayerGUI()
        player_copy.name = self.name
        player_copy.hand = copy.deepcopy(self.hand)
        player_copy.card_history = copy.deepcopy(self.card_history)
        player_copy.chosen_cards = copy.deepcopy(self.chosen_cards)
        player_copy.maki_icons = self.maki_icons
        player_copy.pudding_cards = self.pudding_cards
        player_copy.score = self.score
        player_copy.last_played = copy.deepcopy(self.last_played)
