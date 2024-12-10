import pygame
import random
import time

# 초기화
pygame.init()

# 화면 기본 크기
CARD_WIDTH, CARD_HEIGHT = 100, 150
MARGIN = 10
FONTSIZE = 60
FONT = pygame.font.Font(None, FONTSIZE)

# 색상 정의
BLACK = (0, 0, 0)       # 카드 배경
GREEN = (0, 255, 0)     # 선택
BLUE = (0, 0, 255)      # 일치한 색상
WHITE = (255, 255, 255) # 배경
TEXT_COLOR = (0, 0, 0)  # 텍스트 색상

def createDeck(pairs):
    """단계별 카드 덱 생성 (2쌍, 4쌍 등)."""
    deck = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:pairs])
    deck = deck * 2  # 두 개씩 쌍 생성
    random.shuffle(deck)
    return deck

def drawBoard(screen, board, revealed, matched, cols):
    """카드를 그리는 함수."""
    rows = (len(board) + cols - 1) // cols  # 행 계산
    screen.fill(WHITE)
    
    for i in range(len(board)):
        x = MARGIN + (i % cols) * (CARD_WIDTH + MARGIN)
        y = MARGIN + (i // cols) * (CARD_HEIGHT + MARGIN)

        if matched[i]:
            color = BLUE  # 일치한 카드
        elif revealed[i]:
            color = GREEN  # 선택된 카드
        else:
            color = BLACK  # 기본 카드 배경

        pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))

        # 텍스트 표시
        if revealed[i] or matched[i]:
            text = FONT.render(board[i], True, TEXT_COLOR)
            screen.blit(text, (x + CARD_WIDTH//2 - text.get_width()//2, y + CARD_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()

def displayMessage(screen, message, color, width, height):
    """메시지를 화면에 표시."""
    screen.fill(WHITE)
    text = FONT.render(message, True, color)
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    pygame.display.flip()
    time.sleep(2)

def main():
    level = 1
    max_level = 5
    pairs = 2  # 초기 카드 쌍 수 (2쌍 = 4장)

    # 시작 화면
    screen = pygame.display.set_mode((600, 400))
    displayMessage(screen, "GAME START", TEXT_COLOR, 600, 400)

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_start = False

    while level <= max_level:
        cols = 4 if level < max_level else 5  # 마지막 단계는 5x4
        rows = (pairs * 2 + cols - 1) // cols
        width = MARGIN + cols * (CARD_WIDTH + MARGIN)
        height = MARGIN + rows * (CARD_HEIGHT + MARGIN)
        screen = pygame.display.set_mode((width, height))

        deck = createDeck(pairs)
        revealed = [False] * len(deck)
        matched = [False] * len(deck)
        first_card = None
        matches_found = 0
        can_click = True

        displayMessage(screen, f"{level} stage start!", TEXT_COLOR, width, height)

        runChk = True
        while runChk:
            drawBoard(screen, deck, revealed, matched, cols)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and can_click:  # 좌클릭만 허용
                    x, y = event.pos
                    card_index = (y // (CARD_HEIGHT + MARGIN)) * cols + (x // (CARD_WIDTH + MARGIN))

                    if card_index < len(deck) and not revealed[card_index] and not matched[card_index]:
                        revealed[card_index] = True
                        drawBoard(screen, deck, revealed, matched, cols)

                        if first_card is None:
                            first_card = card_index
                        else:
                            can_click = False
                            if deck[first_card] == deck[card_index]:
                                matches_found += 1
                                matched[first_card] = True
                                matched[card_index] = True
                                first_card = None
                                can_click = True

                                if matches_found == pairs:
                                    if level == max_level:
                                        displayMessage(screen, "Game Complete!", TEXT_COLOR, width, height)
                                        pygame.quit()
                                        return
                                    else:
                                        level += 1
                                        pairs += 2
                                        runChk = False
                            else:
                                time.sleep(1)  # 틀린 카드 확인 시간
                                revealed[first_card] = False
                                revealed[card_index] = False
                                first_card = None
                                can_click = True

if __name__ == "__main__":
    main()
