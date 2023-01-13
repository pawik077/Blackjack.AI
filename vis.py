import pygame
import sys

WINDOW_SIZE = (800, 800)
CARD_SIZE = (80, 120)
CARD_GAP = 20
BG_COLOR = (4, 77, 48)

colsymbol_map = {
    "♠": "spades",
    "♥": "clubs",
    "♦": "hearts",
    "♣": "diamonds",
}

cardsymbol_map = {"K": "king", "Q": "queen", "J": "jack", "A": "ace"}
card_images = {}

player_hand = []
dealer_hand = []


def main():
    # Prepare the window
    pygame.init()
    canvas = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("blackjack")

    # Load card images into memory
    for colkey in colsymbol_map:
        for i in range(2, 11):
            name = f"{i}{colsymbol_map[colkey]}"
            card_images[name] = load_img(name)
        for cardkey in cardsymbol_map:
            name = f"{cardsymbol_map[cardkey]}{colsymbol_map[colkey]}"
            card_images[name] = load_img(name)

    card_images["cardback"] = load_img("cardback")

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            elif event.type == pygame.KEYDOWN:
                advance()

        # clear canvas
        canvas.fill(BG_COLOR)

        draw_hand(canvas, dealer_hand, True)
        draw_hand(canvas, player_hand, False)

        canvas.blit(
            card_images["cardback"],
            (
                WINDOW_SIZE[0] - CARD_GAP - CARD_SIZE[0],
                WINDOW_SIZE[1] / 2 - CARD_SIZE[0] + CARD_GAP,
            ),
        )

        pygame.display.update()


def load_img(name):
    card = pygame.image.load(f"./cards/{name}.png").convert_alpha()
    card = pygame.transform.scale(card, CARD_SIZE)
    return card


def advance():
    global player_hand, dealer_hand

    line = sys.stdin.readline().rstrip().lstrip()
    print(line)

    if line.startswith("Players hand:"):
        player_hand = parse_hand_line(line)
    elif line.startswith("Dealers hand"):
        dealer_hand = parse_hand_line(line)
    elif line.startswith("Round"):
        player_hand.clear()
        dealer_hand.clear()


def parse_hand_line(line):
    tokens = line.split(":")
    # remove whitespace and brackets
    hand_tokens = tokens[1].lstrip().rstrip()
    hand_tokens = hand_tokens.lstrip("[").rstrip("]")
    hand_tokens = hand_tokens.split(", ")

    new_hand = []

    for card in hand_tokens:
        # important
        card = card.lstrip()

        if card == "??":
            card_name = "cardback"
        else:
            card_name = ""
            # if special symbol - translate, otherwise copy number
            if card[0:-1] in cardsymbol_map:
                card_name += cardsymbol_map[card[0:-1]]
            else:
                card_name += card[0:-1]

            card_name += colsymbol_map[card[-1]]

        new_hand.append(card_name)

    return new_hand


def draw_hand(canvas, hand, top=False):
    # it's very unlikely we'll hit this number of cards in player's hand but we need to be prepared anyway
    chunks = [x for x in divide_chunks(hand, 7)]
    for (chunk_i, chunk) in enumerate(chunks):
        # evil math
        first_pos = (
            CARD_GAP
            + (WINDOW_SIZE[0] - 2 * CARD_GAP) / 2
            - (len(chunk) / 2) * CARD_SIZE[0]
            - (len(chunk) / 2 - 0.5) * CARD_GAP
        )

        for (i, card) in enumerate(chunk):
            if top:
                y_coord = CARD_GAP + chunk_i * (CARD_SIZE[1] + CARD_GAP)
            else:
                y_coord = WINDOW_SIZE[1] - (chunk_i + 1) * (CARD_SIZE[1] + CARD_GAP)
            canvas.blit(
                card_images[card],
                (first_pos + i * (CARD_SIZE[0] + CARD_GAP), y_coord),
            )


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


if __name__ == "__main__":
    main()
