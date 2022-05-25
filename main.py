import os
import pygame

pygame.init()

size = (1600, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyGame Launcher')
clock = pygame.time.Clock()

font = pygame.font.Font(None, int(size[1] / 20))

highlighted = 0
games = []
for path in os.listdir('./'):
    full_path = os.path.join('./', path)
    if not os.path.isfile(full_path) and not full_path.__contains__('.DS') and not full_path.__contains__('.idea') and \
            not full_path.__contains__('venv'):
        games.append(f'{path}')

c = 0
highlighted = 0
selected = 0
highlighted_y = 0
highlighted_x = 0


def create_button(text, text_center, button_background_rect, font, text_color='White'):
    button_text = font.render(text, True, text_color)
    button_text_rect = button_text.get_rect(center=text_center)
    button_background = pygame.rect.Rect(button_background_rect)

    return [button_text, button_text_rect, button_background]


def handle_button(button, standard_color=(30, 30, 30), highlighted_color=(100, 100, 100), clicked_color=(255, 255, 255),
                  button_radius=20, click_function=print, function_option='click'):
    mouse_position = pygame.mouse.get_pos()
    pygame.draw.rect(screen, standard_color, button[2], border_radius=button_radius)
    if button[2].collidepoint(mouse_position) and pygame.mouse.get_pressed()[0]:
        pygame.draw.rect(screen, clicked_color, button[2], border_radius=20)
        pygame.mouse.set_pos(mouse_position[0], mouse_position[1] + 100)
        click_function(function_option)
    elif button[2].collidepoint(mouse_position):
        pygame.draw.rect(screen, highlighted_color, button[2], border_radius=20)
    screen.blit(button[0], button[1])


play_button = create_button('Play', (int(size[0] / 8) - 75, int(size[1] / 2) + 100),
                            (int(size[0] / 16) - 75, int(size[1] / 2) + 60, 200, 75), font)
options_button = create_button('...', (int(size[0] / 8) + 75, int(size[1] / 2) + 100),
                               (int(size[0] / 16) + 138, int(size[1] / 2) + 60, 75, 75), font)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if pygame.mouse.get_pos()[0] >= size[0] / 4 and not highlighted >= len(games):
                        selected = highlighted

        games = []
        for path in os.listdir('./'):
            full_path = os.path.join('./', path)
            if not os.path.isfile(full_path) and not full_path.__contains__(
                    '.DS') and not full_path.__contains__('.idea') and \
                    not full_path.__contains__('venv') and not full_path.__contains__('.git'):
                games.append(f'{path}')

        # Get which Game the mouse is over
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] >= int(size[0] / 4):
            highlighted_y = int(mouse_pos[1] / 100)
            highlighted_x = int((mouse_pos[0] - size[0] / 4) / ((size[0] - size[0] / 4) / 4))
            highlighted = (highlighted_y * 4) + highlighted_x

        # Background
        screen.fill(color=(20, 20, 20))
        left_bar_rect = pygame.rect.Rect(0, 0, int(size[0] / 4), size[1])
        pygame.draw.rect(surface=screen, color=(40, 40, 40), rect=left_bar_rect)

        # List games on right side
        square = pygame.rect.Rect(400 + 5, 5, 290, 90)

        i = 0
        for item in games:
            pygame.draw.rect(surface=screen, color=(30, 30, 30), rect=square, border_radius=30)

            if c == highlighted and pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(surface=screen, color=(250, 250, 250), rect=square, border_radius=30)
            elif c == highlighted:
                pygame.draw.rect(surface=screen, color=(100, 100, 100), rect=square, border_radius=30)

            if c == selected:
                pygame.draw.rect(surface=screen, color=(200, 200, 200), rect=square, border_radius=30)

            text = font.render(f'{item}', True, 'White')
            text_rect = text.get_rect(center=square.center)
            screen.blit(text, text_rect)

            square.x += 300

            c += 1
            i += 1
            if i == 4:
                square.x = 405
                square.y += 100
                i = 0
        c = 0

        # Show selected game on left side
        # Does game folder contain game image?
        if not selected >= len(games):
            if os.listdir(f'./{games[selected]}/').__contains__('logo.png'):
                logo_surf = pygame.image.load(f'./{games[selected]}/logo.png').convert_alpha()
                logo_surf = pygame.transform.scale(logo_surf, (int((size[0] / 4) - (size[0] / 16)), int((size[0] / 4) -
                                                                                                        (size[
                                                                                                             0] / 16))))
                logo_rect = logo_surf.get_rect(topleft=(int(size[1] / 21), int(size[1] / 21)))
                background_rect = pygame.rect.Rect(25, 25, 350, 350)
                pygame.draw.rect(screen, (100, 100, 100), background_rect, border_radius=20)
                screen.blit(logo_surf, logo_rect)

            title = font.render(f'{games[selected]}', True, 'White')
            title_rect = title.get_rect(topleft=(25, int(size[1] / 2)))
            screen.blit(title, title_rect)

            handle_button(play_button, click_function=os.system, function_option=f'python {games[selected]}/main.py')
            handle_button(options_button)
        # pygame.draw.line(surface=screen, color='Red', start_pos=(0, highlighted_y * 100), end_pos=(1600,
        # highlighted_y * 100), width=1)
        # pygame.draw.line(surface=screen, color='Red', start_pos=(highlighted_x * ((
        # size[0] - (size[0] / 4)) / 4) + (size[0] / 4), 0), end_pos=(highlighted_x * ((size[0] - (size[ 0] / 4) ) /
        # 4) + ( size[0] / 4), 1000))

        # Update the display
        pygame.display.update()
        clock.tick(60)  # Framerate

except KeyboardInterrupt:
    print('User Interrupt')
