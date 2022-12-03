import random
CARD_SUIT_SYMBOLS = {"Spades": "♠", "Clubs": "♣", "Hearts": "♥", "Diamonds": "♦"}

class Card:
    def __init__(self, suit, rank):
        '''Creates a card with the given suit and rank'''
        self.suit = suit
        self.rank = rank
        self.value = self.getValue()
        self.name = self.getName()
    def getValue(self):
        '''Returns the value of the card'''
        if self.rank == 'A':
            return 11
        elif self.rank == 'J' or self.rank == 'Q' or self.rank == 'K':
            return 10
        else:
            return int(self.rank)
    def getName(self):
        return self.rank + CARD_SUIT_SYMBOLS[self.suit]
    def __repr__(self):
        return self.name

class Deck:
    def __init__(self, seed) -> None:
        '''Constructor'''
        self.cards = []
        self.discarded = []
        self.suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.shuffle(seed)

    def build(self) -> None:
        '''Builds the deck'''
        self.discarded = []
        for s in self.suits:
            for v in self.ranks:
                self.cards.append(Card(s, v))

    def shuffle(self, seed=None) -> None:
        '''Shuffles the deck'''
        random.seed(seed)
        self.build()
        random.shuffle(self.cards)

    def cardinality(self) -> int:
        '''Returns the number of cards in the deck'''
        return len(self.cards)

    def testDeck(self) -> None:
        """Prints the deck to the console (for testing purposes)"""
        for c in self.cards:
            print(c)
        print(len(self.cards))
    
    def deal(self) -> Card:
        '''Deals a card from the deck and adds it to discarded card set'''
        card = random.choice(self.cards)
        self.cards.remove(card)
        self.discarded.append(card)
        return card
    
    def negation(self) -> list:
        '''Returns the negation of the deck'''
        final = []
        for i in range(52):
            final.append(0)
        for card in self.discarded:
            value = card.value
            index = 4 * (value - 1)
            if final[index] == 0:
                final[index] = 1
            elif final[index + 1] == 0:
                final[index + 1] = 1
            elif final[index + 2] == 0:
                final[index + 2] = 1
            elif final[index + 3] == 0:
                final[index + 3] = 1
        return final