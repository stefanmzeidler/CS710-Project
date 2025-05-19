import card

def score_round(players):
    score_maki_cards(players)
    for player in players:
        score_set_cards(player)
        score_other_cards(player)



def score_maki_cards(players):
    maki_cards = sorted(players, key=lambda p: p.maki_icons, reverse=True)
    count = maki_cards_helper(maki_cards)
    points = 6 // count
    for i in range(count):
        maki_cards[0].score += points
        del maki_cards[0]
    if count == 1:
        count = maki_cards_helper(maki_cards)
        points = 3 // count
        for i in range(count):
            maki_cards[0].score += points
            del maki_cards[0]

def count_maki_icons(player, game_round):
    chosen_cards = player.card_history[game_round]
    player.maki_icons = 0
    for chosen_card in chosen_cards:
        match chosen_card.name:
            case card.SINGLE_MAKI:
                player.maki_icons += 1
            case card.DOUBLE_MAKI:
                player.maki_icons += 2
            case card.TRIPLE_MAKI:
                player.maki_icons += 3

def maki_cards_helper(maki_cards):
    top_score = maki_cards[0].maki_icons
    count = 0
    for player in maki_cards:
        if player.maki_icons == top_score:
            count += 1
        else:
            break
    return count

def get_maki_count(chosen_cards):
    maki_count = 0
    for chose_card in chosen_cards:
        match chose_card.name:
            case card.SINGLE_MAKI:
                maki_count += 1
            case card.DOUBLE_MAKI:
                maki_count += 2
            case card.TRIPLE_MAKI:
                maki_count += 3
            case _ :
                continue


def score_pudding_cards(players):
    sorted_players = sorted(players, key=lambda p: p.pudding_cards, reverse=True)
    top_score = sorted_players[0].pudding_cards
    low_score = sorted_players[len(sorted_players) - 1].pudding_cards
    top_scorers = 0
    low_scorers = 0
    for player in sorted_players:
        if player.pudding_cards == top_score:
            top_scorers += 1
        elif player.pudding_cards == low_score:
            low_scorers += 1
    add_score = 6 // top_scorers
    if low_scorers > 0:
        sub_score = 6 // low_scorers
    else:
        sub_score = 0
    for player in players:
        if player.pudding_cards == top_score:
            player.score += add_score
        elif player.pudding_cards == low_score:
            player.score -= sub_score


def score_set_cards(player):
    tempura_cards = sashimi_cards = dumpling_cards = 0
    for chosen_card in player.chosen_cards:
        if chosen_card.name == card.TEMPURA:
            tempura_cards += 1
        elif chosen_card.name == card.SASHIMI:
            sashimi_cards += 1
        elif chosen_card.name == card.DUMPLING:
            dumpling_cards += 1
    if tempura_cards > 0:
        player.score = player.score + (tempura_cards // 2 * 5)
    if sashimi_cards > 0:
        player.score = player.score + (sashimi_cards // 3 * 10)
    if dumpling_cards >= 5:
        player.score = player.score + 15
    match dumpling_cards:
        case 1:
            player.score = player.score + 1
        case 2:
            player.score = player.score + 3
        case 3:
            player.score = player.score + 6
        case 4:
            player.score = player.score + 10

def score_other_cards(player):
    for chosen_card in player.chosen_cards:
        match chosen_card.name:
            case card.SQUID:
                if chosen_card.prev is None:
                    player.score = player.score + 3
            case card.SALMON:
                if chosen_card.prev is None:
                    player.score = player.score + 2
            case card.EGG:
                if chosen_card.prev is None:
                    player.score = player.score + 1
            case card.PUDDING:
                continue
            case card.WASABI:
                if chosen_card.next is None:
                    continue
                elif chosen_card.next.name == card.SQUID:
                    player.score = player.score + 9
                elif chosen_card.next.name == card.SALMON:
                    player.score = player.score + 6
                elif chosen_card.next.name == card.PUDDING:
                    player.score = player.score + 3

def chosen_cards_to_strings(chosen_cards):
    card_list = []
    for chosen_card in chosen_cards:
        card_list.append(str(chosen_card))
    return card_list