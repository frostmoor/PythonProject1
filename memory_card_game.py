import pygame
import random
import time
import os

# Pygame 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Memory Matching Game')

# 칼라
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 카드 설정
CARD_WIDTH, CARD_HEIGHT = 100, 150
MARGIN = 10
FONTSIZE = 60
FONT = pygame.font.Font(None, FONTSIZE)

# 카드 생성
def createDeck():
    deck = list('AABBCCDDEE')
    random.shuffle(deck)
    return deck

def drawBoard(board, revealed):
    screen.fill(WHITE)
    for i in range(10):
        x = MARGIN + (i % 5) * (CARD_WIDTH + MARGIN)
        y = MARGIN + (i // 5) * (CARD_HEIGHT + MARGIN)
        if revealed[i]:
            pygame.draw.rect(screen, GREEN, (x, y, CARD_WIDTH, CARD_HEIGHT))
            text = FONT.render(board[i], True, BLACK)
            screen.blit(text, (x + CARD_WIDTH//2 - text.get_width()//2, y + CARD_HEIGHT//2 - text.get_height()//2))
        else:
            pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT))
    pygame.display.flip()

def check_match(board, first, second):
    return board[first] == board[second]

def main():
    deck = createDeck()
    revealed = [False] * 10
    first_card = None
    matches_found = 0

    runChk = True
    while runChk:
        drawBoard(deck, revealed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runChk = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                card_index = (y // (CARD_HEIGHT + MARGIN)) * 5 + (x // (CARD_WIDTH + MARGIN))
                if not revealed[card_index]:
                    revealed[card_index] = True
                    if first_card is None:
                        first_card = card_index
                    else:
                        if check_match(deck, first_card, card_index):
                            matches_found += 1
                            if matches_found == 5:
                                screen.fill(WHITE)
                                congrats_text = FONT.render('Congrats!!!', True, RED)
                                screen.blit(congrats_text, (WIDTH//2 - congrats_text.get_width()//2, HEIGHT//2 - congrats_text.get_height()//2))
                                pygame.display.flip()
                                time.sleep(2)
                                main()
                        else:
                            time.sleep(1)
                            revealed[first_card] = False
                            revealed[card_index] = False
                        first_card = None

    pygame.quit()

if __name__ == "__main__":
    main()
