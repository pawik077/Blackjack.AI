from Deck import Deck
from Blackjack import handValue

import getopt
import sys
import tensorflow as tf
import numpy as np
from time import time

def test_model(setName: str, iters: int, level: int, debug: bool, shuffle: bool, seed):
    '''Test a model against a set number of iterations of blackjack
    Args:
        setName (str): The name of the model to test
        iters (int): The number of rounds to simulate
        level (int): The level of the model to test
            level 1: only the player's hand value
            level 2: the player's hand value and the dealer's upcard
            level 3: the player's hand value, the dealer's upcard, and the deck's negation (card counting)
        debug (bool): Whether or not to print debug messages
        shuffle (bool): Whether or not to shuffle the deck (needed only for level 3)
        seed (int): The seed to use for shuffling the deck (None for default)'''
    deck = Deck(seed)
    with open(f'models/{setName}.json', 'r') as f:
        model = tf.keras.models.model_from_json(f.read(), custom_objects={'GlorotUniform': tf.keras.initializers.glorot_uniform})
    model.load_weights(f'models/{setName}.h5')
    
    wins = 0
    losses = 0
    ties = 0

    tStart = time()
    for i in range(iters):
        print(f'\rRound {i+1} of {iters}', end='')
        data = []

        if level < 3: deck.shuffle(seed)
        if deck.cardinality() < 10:
            if debug: print('\nShuffling deck')
            deck.shuffle(seed)
        
        dealersHand = [deck.deal(), deck.deal()]
        playersHand = [deck.deal(), deck.deal()]
        if debug: 
            print(f'\nPlayers hand: {playersHand}')
            print(f'Dealers hand: [{dealersHand[0]}, ??]')
        
        sum = handValue(playersHand)

        # if blackjack
        if sum == 21 and handValue(dealersHand) == 21:
            if debug: print("Push")
            ties += 1
            continue
        elif sum == 21 and handValue(dealersHand) != 21:
            if debug: print("Blackjack! Player wins!")
            wins += 1
            continue
        elif sum != 21 and handValue(dealersHand) == 21:
            if debug: print("Dealer has blackjack! Player loses!")
            losses += 1
            continue
        else:
            playersSum = sum
        
        # player's turn
        for i in range(8):
            if level == 1:
                data.append(handValue(playersHand))
            elif level == 2:
                data.append([handValue(playersHand), dealersHand[0].value])
            elif level == 3:
                data.append([handValue(playersHand), dealersHand[0].value] + deck.negation())
            
            prediction = model.predict(np.array(data), verbose=0)
            if prediction[0][0] > prediction[0][1]:
                choice = 's'
            else:
                choice = 'h'
            
            if choice == 'h':
                playersHand.append(deck.deal())
                sum = handValue(playersHand)
                if debug:
                    print('Hitting')
                    print(f'Players hand: {playersHand}')
                    print(f'Dealers hand: {dealersHand[0]}, ??')
                if sum > 21:
                    if debug: print('Player busts! Player loses!')
                    losses += 1
                    break
                elif sum == 21:
                    if debug: print('Player wins!')
                    wins += 1
                    break
                else:
                    playersSum = sum
            else:
                if level == 1:
                    data.append(handValue(playersHand))
                elif level == 2:
                    data.append([handValue(playersHand), dealersHand[0].value])
                elif level == 3:
                    data.append([handValue(playersHand), dealersHand[0].value] + deck.negation())

                if debug: 
                    print('Standing')
                    print(f'Players hand: {playersHand}')
                    print(f'Dealers hand: [{dealersHand[0]}, ??]')
                
                # dealer's turn
                while handValue(dealersHand) < 17:
                    dealersHand.append(deck.deal())
                    if debug: 
                        print('Dealer hits')
                        print(f'Dealers hand: {dealersHand}')
                sum = handValue(dealersHand)
                if sum > 21:
                    if debug: print('Dealer busts! Player wins!')
                    wins += 1
                    break
                elif sum == 21:
                    if debug: print('Dealer wins!')
                    losses += 1
                    break
                else:
                    if debug:
                        print('Dealer stands')
                        print(f'Players hand: {playersHand}')
                        print(f'Dealers hand: {dealersHand}')
                    if sum > playersSum:
                        if debug: print('Dealer wins!')
                        losses += 1
                        break
                    elif sum < playersSum:
                        if debug: print('Player wins!')
                        wins += 1
                        break
                    else:
                        if debug: print('Push')
                        ties += 1
                        break
    tEnd = time()
    return wins, losses, ties, tEnd - tStart


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:d:i:se:b', ['level=', 'dataset=', 'iters=', 'shuffle', 'seed=', 'debug'])
    except getopt.GetoptError as err:
        print(f'Error: {err}')
        sys.exit(2)

    level = 0
    dataset = ''
    iters = 0
    shuffle = False
    debug = False
    seed = None
    
    for o, a in opts:
        if o in ('-l', '--level'):
            level = int(a)
        elif o in ('-d', '--dataset'):
            dataset = a
        elif o in ('-i', '--iters'):
            iters = int(a)
        elif o in ('-s', '--shuffle'):
            shuffle = True
        elif o in ('-e', '--seed'):
            seed = int(a)
        elif o in ('-b', '--debug'):
            debug = True
    if level == 0 or dataset == '' or iters == 0:
        print('Usage: python3 test.py -l <level> -d <dataset> -i <iters> [-s] [-e <seed>]')
        sys.exit(1)
    else:
        # deck = Deck(seed)
        wins, losses, ties, duration = test_model(dataset, iters, level, debug, shuffle, seed)
        print(f'\rFinished in : {duration:.2f} seconds ({((duration) / iters * 1000):.5f} milliseconds per iteration)')
        print(f'Wins: {wins}, Losses: {losses}, Ties: {ties}')
        print(f'Win rate: {(wins / iters * 100):.2f}%')
        print(f'Win-to-loss ratio: {(wins / losses):.2f}')