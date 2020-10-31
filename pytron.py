import pygame
import time
pygame.init()

BLACK = (0, 0, 0)
P1_COLOR = (0, 255, 255)
P2_COLOR = (255, 0, 255)

class Player:
    def __init__(self, x, y, b, c):
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = b
        self.color = c
        self.boost = False
        self.start_boost = time.time()
        self.boosts = 3
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)

    def __draw__(self):
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)
        pygame.draw.rect(screen, self.color, self.rect, 0)

    def __move__(self):
        if not self.boost:
            self.x += self.direction[0]
            self.y += self.direction[1]
        else:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2

    def __boost__(self):
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


def new_game():
    new_p1 = Player(50, height / 2, (2, 0), P1_COLOR)
    new_p2 = Player(width - 50, height / 2, (-2, 0), P2_COLOR)
    return new_p1, new_p2


width = 600
height = 660
offset = height - width
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyTron")

font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()
check_time = time.time()

objects = list()
path = list()
p1 = Player(50, (height- offset) / 2, (2, 0), P1_COLOR)
p2 = Player(width - 50, (height- offset) / 2, (-2, 0), P2_COLOR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))

player_score = [0, 0]

wall_rects = [pygame.Rect([0, offset, 15, height]) , pygame.Rect([0, offset, width, 15]),
              pygame.Rect([width - 15, offset, 15, height]),
              pygame.Rect([0, height - 15, width, 15])]

done = False
new = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # player 1
            if event.key == pygame.K_w:
                objects[0].direction = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].direction = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].direction = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].direction = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            # player 2
            if event.key == pygame.K_UP:
                objects[1].direction = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].direction = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].direction = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].direction = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()

    screen.fill(BLACK)

    for r in wall_rects: pygame.draw.rect(screen, (42, 42, 42), r, 0)

    for o in objects:
        if time.time() - o.start_boost >= 0.5:
            o.boost = False

        if (o.rect, '1') in path or (o.rect, '2') in path \
           or o.rect.collidelist(wall_rects) > -1:
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()

                if o.color == P1_COLOR:
                    player_score[1] += 1
                else: player_score[0] += 1

                new = True
                new_p1, new_p2 = new_game()
                objects = [new_p1, new_p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
                break
        else:
            path.append((o.rect, '1')) if o.color == P1_COLOR else path.append((o.rect, '2'))

        o.__draw__()
        o.__move__()

    for r in path:
        if new is True:
            path = []
            new = False
            break
        if r[1] == '1': pygame.draw.rect(screen, P1_COLOR, r[0], 0)
        else: pygame.draw.rect(screen, P2_COLOR, r[0], 0)

    score_text = font.render('{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 153, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(width / 2)
    score_text_pos.centery = int(offset / 2)
    screen.blit(score_text, score_text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
