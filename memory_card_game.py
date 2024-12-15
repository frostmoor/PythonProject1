import pygame
import random
import time
import os

# 초기화
pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('메모리 카드 게임')

# 칼라
BLACK = (0, 0, 0)  # 카드 배경
GREEN = (0, 255, 0)  # 선택
BLUE = (0, 0, 255)  # 일치한 색상
WHITE = (255, 255, 255)  # 배경
RED = (255, 0, 0)  # 축하

# 카드 설정
CARD_WIDTH, CARD_HEIGHT = 100, 150
MARGIN = 10
FONTSIZE = 60
FONT = pygame.font.Font(None, FONTSIZE)


# 카드 생성
def createDeck(card_count):
    deck = list('AABBCCDDEEFFGGHHIIJJ'[:card_count])
    random.shuffle(deck)
    return deck


# 보드 그리기
def drawBoard(board, revealed, matched):
    screen.fill(WHITE)
    for i in range(len(board)):
        x = MARGIN + (i % 5) * (CARD_WIDTH + MARGIN)
        y = MARGIN + (i // 5) * (CARD_HEIGHT + MARGIN)

        if matched[i]:
            color = BLUE
        elif revealed[i]:
            color = GREEN
        else:
            color = BLACK

        pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))

        if revealed[i] or matched[i]:
            text = FONT.render(board[i], True, BLACK)
            screen.blit(text, (x + CARD_WIDTH // 2 - text.get_width() // 2,
                               y + CARD_HEIGHT // 2 - text.get_height() // 2))
    draw_timer()
    draw_score()
    pygame.display.flip()


# 애니메이션
def flip_animation(card_index):
    x = MARGIN + (card_index % 5) * (CARD_WIDTH + MARGIN)
    y = MARGIN + (card_index // 5) * (CARD_HEIGHT + MARGIN)
    for scale in range(1, 6):
        pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(screen, BLACK,
                         (x + scale * 10, y, CARD_WIDTH - scale * 20, CARD_HEIGHT))
        pygame.display.flip()
        time.sleep(0.05)


# 점수
score = 0


def update_score(points):
    global score
    score += points


def draw_score():
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


# 타이머
start_time = time.time()


def draw_timer():
    elapsed_time = int(time.time() - start_time)
    timer_text = FONT.render(f"Time: {elapsed_time}s", True, BLACK)
    screen.blit(timer_text, (WIDTH - 150, 10))


# 매칭 확인
def check_match(board, first, second):
    return board[first] == board[second]


# 난이도 선택
def choose_difficulty():
    screen.fill(WHITE)
    easy_text = FONT.render('1. Easy (10 cards)', True, BLACK)
    medium_text = FONT.render('2. Medium (20 cards)', True, BLACK)
    hard_text = FONT.render('3. Hard (30 cards)', True, BLACK)

    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10
                elif event.key == pygame.K_2:
                    return 20
                elif event.key == pygame.K_3:
                    return 30


# 메인 게임
def main():
    global score, start_time
    card_count = choose_difficulty()
    deck = createDeck(card_count)
    revealed = [False] * card_count
    matched = [False] * card_count
    first_card = None
    matches_found = 0
    can_click = True

    start_time = time.time()  # 타이머 초기화
    score = 0  # 점수 초기화

    runChk = True
    while runChk:
        drawBoard(deck, revealed, matched)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runChk = False

            elif event.type == pygame.MOUSEBUTTONDOWN and can_click:
                x, y = event.pos
                card_index = (y // (CARD_HEIGHT + MARGIN)) * 5 + (x // (CARD_WIDTH + MARGIN))
                if card_index < card_count and not revealed[card_index] and not matched[card_index]:
                    flip_animation(card_index)
                    revealed[card_index] = True
                    drawBoard(deck, revealed, matched)

                    if first_card is None:
                        first_card = card_index
                    else:
                        can_click = False  # 클릭 잠금
                        if check_match(deck, first_card, card_index):
                            update_score(10)  # 점수 추가
                            matches_found += 1
                            matched[first_card] = True
                            matched[card_index] = True
                            first_card = None
                            can_click = True

                            if matches_found == card_count // 2:
                                screen.fill(WHITE)
                                congrats_text = FONT.render('Congrats!!!', True, RED)
                                screen.blit(congrats_text,
                                            (WIDTH // 2 - congrats_text.get_width() // 2,
                                             HEIGHT // 2 - congrats_text.get_height() // 2))
                                pygame.display.flip()
                                time.sleep(2)
                                main()
                        else:
                            update_score(-5)  # 점수 차감
                            pygame.display.flip()
                            time.sleep(2)  # 2초 대기
                            revealed[first_card] = False
                            revealed[card_index] = False
                            drawBoard(deck, revealed, matched)
                            first_card = None
                            can_click = True

    pygame.quit()


if __name__ == "__main__":
    main()
