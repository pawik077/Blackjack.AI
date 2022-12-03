from Deck import Deck

import random as rd
from time import time
import getopt
import os
import sys

# deck = Deck()

def handValue(hand):
    '''Returns the value of a hand'''
    value = 0
    for card in hand:
        value += card.value
    c = 0
    while value > 21 and c < len(hand):
        if hand[c].rank == 'A':
            value -= 10
        c += 1
    return value

def round(montecarlo: bool, level: int, debug: bool, seed):
    '''Play a single round of blackjack
    Args:
        montecarlo (bool): Whether to use montecarlo simulation
        level (int): The level of montecarlo simulation
            level 1: gather data about the player's hand
            level 2: gather level 1 and data about the dealer's hand
            level 3: gather level 2 and the history of seen cards (card counting)
        debug (bool): Whether to print debug messages'''
    # data collection lists
    data = []
    tags = []
    if level < 3: deck.shuffle(seed) # shuffle the deck if we're not counting cards
    if deck.cardinality() < 10: 
        if debug: print("Shuffling deck")
        deck.shuffle(seed) # shuffle the deck if there are less than 10 cards left
    choices = ['h', 's']

    # initial deal
    dealersHand = [deck.deal(), deck.deal()]
    playersHand = [deck.deal(), deck.deal()]
    if debug:
        print(f"Player's hand: {playersHand}")
        print(f"Dealer's hand: [{dealersHand[0]}, ??]")
    
    sum = handValue(playersHand)
    
    # if blackjack
    if sum == 21 and handValue(dealersHand) == 21:
        if debug: print("Push")
        return data, tags
    elif sum == 21 and handValue(dealersHand) != 21:
        if debug: print("Blackjack! Player wins!")
        return data, tags
    elif sum != 21 and handValue(dealersHand) == 21:
        if debug: print("Dealer has blackjack! Player loses!")
        return data, tags
    else:
        playersSum = sum

    # player's turn
    for i in range(8):
        if montecarlo:
            choice = rd.choice(choices)
        else:
            choice = input("Hit or stand? (h/s) ")
            while choice not in choices:
                choice = input("Invalid input. Hit or stand? (h/s) ")
        if choice == 'h':
            if level == 1:
                data.append(handValue(playersHand))
            elif level == 2:
                data.append([handValue(playersHand), dealersHand[0].value])
            elif level == 3:
                data.append([handValue(playersHand), dealersHand[0].value] + deck.negation())
            playersHand.append(deck.deal())
            sum = handValue(playersHand)
            if debug:
                print("Hitting")
                print(f"Player's hand: {playersHand}")
                print(f"Dealer's hand: {dealersHand[0]}, ??")
            if sum > 21:
                tags.append('s')
                if debug: print("Player busts! Player loses!")
                return data, tags
            elif sum == 21:
                tags.append('h')
                if debug: print('Player wins!')
                return data, tags
            else:
                tags.append('h')
                playersSum = sum
        else:
            if level == 1:
                data.append(handValue(playersHand))
            elif level == 2:
                data.append([handValue(playersHand), dealersHand[0].value])
            elif level == 3:
                data.append([handValue(playersHand), dealersHand[0].value] + deck.negation())
            if debug:
                print("Standing")
                print(f"Player's hand: {playersHand}")
                print(f"Dealer's hand: {dealersHand[0]}, ??")
            # dealer's turn
            while handValue(dealersHand) < 17:
                dealersHand.append(deck.deal())
            if debug:
                print("Dealer hits")
                print(f"Player's hand: {playersHand}")
                print(f"Dealer's hand: {dealersHand}")
            sum = handValue(dealersHand)
            if sum > 21:
                tags.append('s')
                if debug: print("Dealer busts! Player wins!")
                return data, tags
            elif sum == 21:
                tags.append('h')
                if debug: print('Dealer wins!')
                return data, tags
            else:
                if debug: 
                    print("Dealer stands")
                    print(f"Player's hand: {playersHand}")
                    print(f"Dealer's hand: {dealersHand}")
                if sum > playersSum:
                    tags.append('h')
                    if debug: print("Dealer wins!")
                    return data, tags
                else:
                    tags.append('s')
                    if debug: print("Player wins!")
                    return data, tags

def genDataSet(iters: int, output: str, level: int, shuffle: bool, seed):
    '''Generate a dataset of blackjack rounds
    Args:
        iters (int): The number of rounds to simulate
        output (str): The name of the output file
        level (int): The level of montecarlo simulation
            level 1: gather data about the player's hand
            level 2: gather level 1 and data about the dealer's hand
            level 3: gather level 2 and the history of seen cards (card counting)
        shuffle (bool): Whether to shuffle the deck before each round (needed only for level 3)'''
    tStart = time()
    os.makedirs('datasets', exist_ok=True)
    for i in range(iters):
        print(f'\rProcessing {i + 1} out of {iters}...', end='')
        try:
            data, tags = round(True, level, False, seed)
            if len(data) != len(tags):
                print("Error: data and tags are not the same length")
                print(data)
                print(tags)
                return
            with open('datasets/' + output + '.data', 'a') as dataFile:
                for datum in data:
                    dataFile.write(str(datum) + '\n')
            with open('datasets/' + output + '.tags', 'a') as tagFile:
                for tag in tags:
                    tagFile.write(tag + '\n')
            # shuffle the deck if enabled
            if shuffle:
                deck.shuffle(seed)
        except Exception as ex:
            print(ex)
            deck.shuffle(seed)
    tEnd = time()
    print(f'\rFinished in {(tEnd - tStart):.2f} seconds ({((tEnd - tStart) / iters * 1000):.5f} milliseconds per round)')

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'pgi:o:l:se:', ['play', 'generate', 'iters=', 'output=', 'level=', 'shuffle', 'seed='])
    except getopt.GetoptError as err:
        print(f'Error: {err}')
        exit(2)

    iters = 0
    output = ''
    level = 0
    shuffle = False
    play = False
    generate = False
    seed = None

    for o,a in opts:
        if o in ('-p', '--play'):
            play = True
        elif o in ('-g', '--generate'):
            generate = True
        elif o in ('-i', '--iters'):
            iters = int(a)
        elif o in ('-o', '--output'):
            output = a
        elif o in ('-l', '--level'):
            level = int(a)
        elif o in ('-s', '--shuffle'):
            shuffle = True
        elif o in ('-e', '--seed'):
            seed = int(a)

    if play and generate:
        print("Error: cannot play and generate at the same time")
    elif play:
        if iters != 0 or output != '' or level != 0 or shuffle:
            print("Error: cannot play and generate at the same time")
        else:
            deck = Deck(seed)
            round(False, 0, True, seed)
    elif generate:
        if iters == 0 or output == '' or level not in (1, 2, 3):
            print("Error: invalid arguments")
            print("Usage: python3 blackjack.py [-p | -g] [-i <iters>] [-o <output>] [-l <level>] [-s] [-e]")
        else:
            deck = Deck(seed)
            genDataSet(iters, output, level, shuffle, seed)
    else:
        print("Usage: python3 blackjack.py [-p | -g] [-i <iters>] [-o <output>] [-l <level>] [-s] [-e]")
