import pygame
from pygame.locals import *
import Costants as const
import Game_logic as Gl


def draw(screen, game_mode, game_l):
    if game_mode == 'l':
        mod = const.light_mod
    else:
        mod = const.dark_mod
    screen.fill(mod['back'])
    text = pygame.font.SysFont(const.font, const.font_size).render(f'Score: {game_l.score}', True, mod['score'])
    text_rect = pygame.Rect(20, 530, 100, 50)
    screen.blit(text, text_rect)
    for i in range(const.N):
        for j in range(const.N):
            n = game_l.copy_grid()[i][j]

            x = j * const.W // const.N + 10
            y = i * const.H // const.N + 10
            w = const.W // const.N - 2 * 10
            h = const.H // const.N - 2 * 10

            pygame.draw.rect(screen,
                             mod[n],
                             pygame.Rect(x, y, w, h),
                             border_radius=15)
            if n == 0:
                continue
            text = pygame.font.SysFont(const.font, const.font_size).render(f'{n}', True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + w / 2, y + h / 2))
            screen.blit(text, text_rect)


def game_over(screen, game_mode, game_l):
    if game_mode == 'l':
        mod = const.light_mod
    else:
        mod = const.dark_mod
    screen.fill(mod['back'])
    text1 = pygame.font.SysFont(const.font, const.font_size).render(f'Game over!!', True, mod['score'])
    text2 = pygame.font.SysFont(const.font, const.font_size).render(f'Score: {game_l.score}', True, mod['score'])
    text_rect1 = pygame.Rect(80, 200, 50, 50)
    text_rect2 = pygame.Rect(80, 250, 50, 50)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)


def win(screen, game_mode):
    if game_mode == 'l':
        mod = const.light_mod
    else:
        mod = const.dark_mod
    screen.fill(mod['back'])

    text = pygame.font.SysFont(const.font, const.font_size).render(f'Good Game !!', True, mod['score'])
    text_rect = pygame.Rect(80, 200, 50, 50)

    screen.blit(text, text_rect)


def wait_command():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    return 'up'
                elif event.key == K_RIGHT:
                    return 'right'
                elif event.key == K_LEFT:
                    return 'left'
                elif event.key == K_DOWN:
                    return 'down'
                elif event.key == K_r:
                    return 'restart'
                elif event.key == K_m:
                    return 'change mod'
                elif event.key == K_q or event.key == K_ESCAPE:
                    return 'quit'


def main():
    pygame.init()
    pygame.display.set_caption("2048")
    screen = pygame.display.set_mode((const.W, const.H+100))
    game_l = Gl.Game2048()
    mod = 'l'
    draw(screen=screen, game_mode=mod, game_l=game_l)
    pygame.display.flip()
    while True:
        command = wait_command()
        if command == 'quit':
            break
        elif command in const.moves and game_l.move_possible(command):
            game_l.make_move(move=command)
        elif command == 'change mod':
            mod = 'l' if mod == 'b' else 'b'

        if game_l.game_over():
            game_over(screen=screen, game_mode=mod, game_l=game_l)
        elif game_l.win():
            win(screen=screen, game_mode=mod)
        else:
            draw(screen=screen, game_mode=mod, game_l=game_l)
        pygame.display.flip()


if __name__ == "__main__":
    main()
