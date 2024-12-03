import pygame
import random
import time
import os

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('메모리 카드 게임')

# 칼라
BLACK = (0, 0, 0)       # 카드 배경
GREEN = (0, 255, 0)     # 선택
BLUE = (0, 0, 255)      # 일치한 색상
WHITE = (255, 255, 255) # 배경
RED = (255, 0, 0)       # 축하

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

def drawBoard(board, revealed, matched):
    screen.fill(WHITE)
    for i in range(10):
        x = MARGIN + (i % 5) * (CARD_WIDTH + MARGIN)
        y = MARGIN + (i // 5) * (CARD_HEIGHT + MARGIN)

        if matched[i]:
            color = BLUE  # 일치하면 BLUE 색상 사용
        elif revealed[i]:
            color = GREEN
        else:
            color = BLACK

        pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))

        if revealed[i] or matched[i]:
            text = FONT.render(board[i], True, BLACK)
            screen.blit(text, (x + CARD_WIDTH//2 - text.get_width()//2, y + CARD_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()

def check_match(board, first, second):
    return board[first] == board[second]

def main():
    deck = createDeck()
    revealed = [False] * 10
    matched = [False] * 10  # 매칭된 카드를 저장하는 리스트
    first_card = None
    matches_found = 0
    can_click = True  # 클릭 가능 여부 플래그

    runChk = True
    while runChk:
        drawBoard(deck, revealed, matched)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runChk = False

            elif event.type == pygame.MOUSEBUTTONDOWN and can_click:
                x, y = event.pos
                card_index = (y // (CARD_HEIGHT + MARGIN)) * 5 + (x // (CARD_WIDTH + MARGIN))

                if not revealed[card_index] and not matched[card_index]:
                    revealed[card_index] = True
                    drawBoard(deck, revealed, matched)

                    if first_card is None:
                        first_card = card_index
                    else:

                        can_click = False  # 두 번째 카드 선택 후 클릭 방지 플래그
                        if check_match(deck, first_card, card_index):
                            matches_found += 1
                            matched[first_card] = True
                            matched[card_index] = True
                            first_card = None
                            can_click = True  # 다시 클릭 가능

                            if matches_found == 5:
                                screen.fill(WHITE)
                                congrats_text = FONT.render('Congrats!!!', True, RED)
                                screen.blit(congrats_text, (WIDTH//2 - congrats_text.get_width()//2, HEIGHT//2 - congrats_text.get_height()//2))
                                pygame.display.flip()

                                time.sleep(2)
                                main()
                        else:
                            pygame.display.flip()
                            time.sleep(2) #2초간의 확인 딜레이
                            revealed[first_card] = False
                            revealed[card_index] = False
                            drawBoard(deck, revealed, matched)
                            first_card = None

                            can_click = True  # 다시 클릭 가능



    pygame.quit()


if __name__ == "__main__":
    main()



