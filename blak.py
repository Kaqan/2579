from itertools import combinations

# İskambil kartlarının listesi ve Blackjack değerleri
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
    deck = []

    for suit in suits:
        for rank, value in ranks.items():
            deck.append((f'{rank} of {suit}', value))
    
    return deck

# Blackjack elini hesaplama
def calculate_hand_value(hand):
    value = sum(card[1] for card in hand)
    ace_count = sum(1 for card in hand if card[0].startswith('Ace'))
    
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    
    return value

# Kurpiyerin elini tamamlama
def dealer_play(dealer_hand, deck):
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop(0))
    return calculate_hand_value(dealer_hand)

# Sonucu değerlendirme
def evaluate_game(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return "Dealer Wins"
    elif dealer_value > 21 or player_value > dealer_value:
        return "Player Wins"
    elif player_value < dealer_value:
        return "Dealer Wins"
    else:
        return "Push"

# Deste sayısını kullanıcıdan alma
num_decks = int(input("Kaç deste istersiniz? "))
full_deck = create_deck() * num_decks

# Tüm kombinasyonları saklamak için liste
results = []
player_wins = 0
dealer_wins = 0

# Oyuncu kombinasyonlarını oluşturma
player_combinations = list(combinations(full_deck, 2))

# Tüm olasılıkları değerlendirme
for player_hand in player_combinations:
    remaining_deck = full_deck.copy()
    remaining_deck.remove(player_hand[0])
    remaining_deck.remove(player_hand[1])
    
    dealer_combinations = list(combinations(remaining_deck, 2))
    
    for dealer_hand in dealer_combinations:
        temp_deck = remaining_deck.copy()
        temp_deck.remove(dealer_hand[0])
        temp_deck.remove(dealer_hand[1])
        
        # Oyuncu Stand Yaparsa
        dealer_final_hand = list(dealer_hand)  # Tuple'ı listeye çeviriyoruz
        dealer_value = dealer_play(dealer_final_hand, temp_deck.copy())
        result = evaluate_game(player_hand, dealer_final_hand)
        results.append({'Player Hand': player_hand, 'Dealer Hand': dealer_hand, 'Result': result, 'Player Action': 'Stand'})
        
        if result == "Player Wins":
            player_wins += 1
        elif result == "Dealer Wins":
            dealer_wins += 1

        # Oyuncu Hit Yaparsa
        for next_card in temp_deck:
            new_player_hand = list(player_hand) + [next_card]
            remaining_deck_after_hit = temp_deck.copy()
            remaining_deck_after_hit.remove(next_card)
            
            dealer_final_hand_after_hit = list(dealer_hand)  # Tuple'ı listeye çeviriyoruz
            dealer_value_after_hit = dealer_play(dealer_final_hand_after_hit, remaining_deck_after_hit.copy())
            result_after_hit = evaluate_game(new_player_hand, dealer_final_hand_after_hit)
            results.append({'Player Hand': new_player_hand, 'Dealer Hand': dealer_hand, 'Result': result_after_hit, 'Player Action': 'Hit'})
            
            if result_after_hit == "Player Wins":
                player_wins += 1
            elif result_after_hit == "Dealer Wins":
                dealer_wins += 1

# Sonuçları yazdırma
for result in results:
    print(f"Player Hand: {result['Player Hand']}, Dealer Hand: {result['Dealer Hand']}, Result: {result['Result']}, Player Action: {result['Player Action']}")

# Toplam oyun sayısı ve kazananların sayısı
print(f"\nToplam oyun sayısı: {len(results)}")
print(f"Player Wins: {player_wins}")
print(f"Dealer Wins: {dealer_wins}")
print(f"Pushes: {len(results) - player_wins - dealer_wins}")
