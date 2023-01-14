import pygame
import sys
import time

WINDOW_SIZE = (800, 800)
CARD_SIZE = (80, 120)
CARD_GAP = 20
BG_COLOR = (4, 77, 48)
FONT_SIZE = 32
SMALL_FONT_SIZE = 16

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

c_round = None
total_rounds = None
status = ""


def main():
    app_state = "WELCOME"

    # Prepare the window
    pygame.init()
    canvas, font, small_font = init()

    while app_state != "QUITTING":
        if app_state == "WELCOME":
            app_state = welcome_screen_loop(canvas, font, small_font)
        elif app_state == "FINISHED":
            app_state = finished_screen_loop(canvas, font, small_font)
            pass
        elif app_state == "MAIN_AA":
            app_state = main_event_loop(canvas, font, small_font, True)
        else:
            app_state = main_event_loop(canvas, font, small_font, False)


def init():
    font = pygame.font.Font("OpenSans-Medium.ttf", FONT_SIZE)
    small_font = pygame.font.Font("OpenSans-Medium.ttf", SMALL_FONT_SIZE)

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
    return canvas, font, small_font


def load_img(name):
    card = pygame.image.load(f"./cards/{name}.png").convert_alpha()
    card = pygame.transform.scale(card, CARD_SIZE)
    return card


def welcome_screen_loop(canvas, font, small_font):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUITTING"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Starting with auto-advance")
                    return "MAIN_AA"
                elif event.key == pygame.K_SPACE:
                    print("Starting without auto-advance")
                    return "MAIN"

        canvas.fill(BG_COLOR)
        draw_deck(canvas)

        lines = [
            "To start without auto-advance press Space",
            "To start with auto-advance press Enter,",
            "Auto-advance moves to next turn in regular periods of time (0.2s default),",
            "Use +/- to increase/decrease that time.",
            "You can always press Enter to disable/enable auto-advance",
            "and use Space to continue manually",
        ]

        for (i, line) in enumerate(lines):
            text = small_font.render(
                line,
                True,
                "white",
                None,
            )
            canvas.blit(text, (100, WINDOW_SIZE[1] / 3 + i * FONT_SIZE))

        pygame.display.update()


def finished_screen_loop(canvas, font, small_font):
    finished_info = status
    wlt = sys.stdin.readline().rstrip().lstrip()
    wr = sys.stdin.readline().rstrip().lstrip()
    wlr = sys.stdin.readline().rstrip().lstrip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUITTING"

        canvas.fill(BG_COLOR)

        draw_hand(canvas, dealer_hand, True)
        draw_hand(canvas, player_hand, False)
        draw_deck(canvas)

        text = font.render(f"Finished!", True, "white", None)
        canvas.blit(text, (20, WINDOW_SIZE[1] / 3 - FONT_SIZE / 2))

        lines = [
            finished_info,
            wlt,
            wr,
            wlr,
        ]

        for (i, line) in enumerate(lines):
            text = small_font.render(
                line,
                True,
                "white",
                None,
            )
            canvas.blit(text, (100, WINDOW_SIZE[1] / 2 + i * FONT_SIZE))

        pygame.display.update()


def main_event_loop(canvas, font, small_font, auto_advance=False):
    start_time = time.time()
    auto_advance_time = 1.0
    adv = "CONT"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUITTING"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    auto_advance_time += 0.2
                    print(f"auto advance time: {auto_advance_time}")
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    auto_advance_time = max(auto_advance_time - 0.2, 0.1)
                    print(f"auto advance time: {auto_advance_time}")
                elif event.key == pygame.K_RETURN:
                    auto_advance = not auto_advance
                    print(f"auto advance: {auto_advance}")
                elif event.key == pygame.K_SPACE:
                    start_time = time.time()
                    adv = advance()

        if auto_advance and time.time() - start_time > auto_advance_time:
            start_time = time.time()
            adv = advance()

        # game finished
        if adv != "CONT":
            return "FINISHED"

        # clear canvas
        canvas.fill(BG_COLOR)

        draw_hand(canvas, dealer_hand, True)
        draw_hand(canvas, player_hand, False)
        draw_deck(canvas)

        print_info(canvas, font)

        pygame.display.update()


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


def draw_deck(canvas):
    canvas.blit(
        card_images["cardback"],
        (
            WINDOW_SIZE[0] - CARD_GAP - CARD_SIZE[0],
            WINDOW_SIZE[1] / 2 - CARD_SIZE[0] + CARD_GAP,
        ),
    )


def print_info(canvas, font):
    if c_round is not None:
        text = font.render(f"Round {c_round} of {total_rounds}", True, "white", None)
        canvas.blit(text, (20, WINDOW_SIZE[1] / 2 - FONT_SIZE / 2))
    text = font.render(status, True, "white", None)
    canvas.blit(text, (20, WINDOW_SIZE[1] / 2 + FONT_SIZE))


def advance(num=1):
    global player_hand, dealer_hand, c_round, total_rounds, status

    i = 0
    while i < num:
        line = sys.stdin.readline().rstrip().lstrip()
        print(line)

        if line.startswith("Players hand:"):
            player_hand = parse_hand_line(line)
        elif line.startswith("Dealers hand"):
            dealer_hand = parse_hand_line(line)
        elif line.startswith("Round"):
            tokens = line.split()
            c_round = int(tokens[1])
            total_rounds = int(tokens[3])
            player_hand.clear()
            dealer_hand.clear()
            status = ""
            advance(2)
        elif line == "Shuffling deck":
            advance(2)
            status = "Deck has been shuffled"
        elif line == "Standing" or line == "Dealer stands":
            advance(2)
            status = line
        elif line == "Hitting" or line == "Dealer hits":
            advance(2)
            status = line
        elif line.startswith("Finished"):
            status = line
            return "END"
        else:
            status = line

        i += 1

    return "CONT"


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


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


if __name__ == "__main__":
    main()
