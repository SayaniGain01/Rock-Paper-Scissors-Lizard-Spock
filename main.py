import pygame
import random

pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock-Paper-Scissors-Lizard-Spock")

# Load images
rock_img = pygame.image.load("images/rock.png")
paper_img = pygame.image.load("images/paper.png")
scissors_img = pygame.image.load("images/scissors.png")
lizard_img = pygame.image.load("images/lizard.png")
spock_img = pygame.image.load("images/spock.png")
background_img = pygame.image.load("images/bg.jpg")

background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont("OCR A Extended", 16, bold=True)
button_font = pygame.font.SysFont("OCR A Extended", 20, bold=True)

# Play button
play_button = pygame.Rect(WIDTH // 2 - 50, 20, 100, 40)

# Rules text
rules = [
    "Scissors cut Paper",
    "Paper covers Rock",
    "Rock crushes Lizard",
    "Lizard poisons Spock",
    "Spock smashes Scissors",
    "Scissors decapitate Lizard",
    "Lizard eats Paper",
    "Paper disproves Spock",
    "Spock vaporizes Rock",
    "Rock crushes Scissors"
]

# Sign images dict
sign_images = {
    "rock": rock_img,
    "paper": paper_img,
    "scissors": scissors_img,
    "lizard": lizard_img,
    "spock": spock_img
}

# Small icons for selection buttons
icon_size = (50, 50)
icons = {}
for name, img in sign_images.items():
    icons[name] = pygame.transform.smoothscale(img, icon_size)

# Create icon button rects
icon_buttons = []
start_x = WIDTH // 2 - (len(icons) * (icon_size[0] + 10)) // 2
y_pos = HEIGHT - icon_size[1] - 20
for i, name in enumerate(icons.keys()):
    rect = pygame.Rect(start_x + i * (icon_size[0] + 10), y_pos, icon_size[0], icon_size[1])
    icon_buttons.append((name, rect))


def draw_main_screen():
    screen.blit(background_img, (0, 0))
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    pygame.draw.rect(screen,(0,0,0),play_button,2)

    #render text with border
    text = button_font.render("PLAY", True, (0,0,0))
    text_rect = text.get_rect(center=play_button.center)
    screen.blit(text, text_rect)
    pygame.display.flip()


def show_rules_popup():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    popup_rect = pygame.Rect(50, 50, 500, 300)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    for i, line in enumerate(rules):
        line_text = font.render(line, True, (0, 0, 0))
        text_width = line_text.get_width()
        x_center = popup_rect.centerx - text_width // 2
        y_position = popup_rect.y + 20 + i * 22
        screen.blit(line_text, (x_center, y_position))

    ok_button = pygame.Rect(popup_rect.centerx - 40, popup_rect.bottom - 50, 80, 30)
    pygame.draw.rect(screen, (0, 200, 0), ok_button)
    pygame.draw.rect(screen, (0, 0, 0), ok_button,2)
    ok_text = button_font.render("OK", True, (0,0,0))
    ok_rect = ok_text.get_rect(center=ok_button.center)
    screen.blit(ok_text, ok_rect)

    pygame.display.flip()

    waiting_for_ok = True
    while waiting_for_ok:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.collidepoint(event.pos):
                    waiting_for_ok = False


def show_sign_selection():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    popup_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    instr = font.render("Choose your sign:", True, (0, 0, 0))
    screen.blit(instr, (popup_rect.x + 20, popup_rect.y + 20))

    for name, rect in icon_buttons:
        screen.blit(icons[name], rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    pygame.display.flip()


def get_winner(user, cooper):
    win_map = {
        "scissors": {"paper": "Scissors cut Paper", "lizard": "Scissors decapitate Lizard"},
        "paper": {"rock": "Paper covers Rock", "spock": "Paper disproves Spock"},
        "rock": {"lizard": "Rock crushes Lizard", "scissors": "Rock crushes Scissors"},
        "lizard": {"spock": "Lizard poisons Spock", "paper": "Lizard eats Paper"},
        "spock": {"scissors": "Spock smashes Scissors", "rock": "Spock vaporizes Rock"}
    }

    if user == cooper:
        return "tie", ""
    elif cooper in win_map[user]:
        return "user", win_map[user][cooper]
    else:
        return "cooper", win_map[cooper][user]


def draw_choices(user_choice, cooper_choice):
    screen.fill((255, 255, 255))

    big_size = (150, 150)
    user_img = pygame.transform.smoothscale(sign_images[user_choice], big_size)
    cooper_img = pygame.transform.smoothscale(sign_images[cooper_choice], big_size)

    user_pos = (WIDTH // 4 - big_size[0] // 2, HEIGHT // 2 - big_size[1] // 2)
    cooper_pos = (3 * WIDTH // 4 - big_size[0] // 2, HEIGHT // 2 - big_size[1] // 2)

    screen.blit(user_img, user_pos)
    screen.blit(cooper_img, cooper_pos)

    user_text = font.render("You", True, (0, 0, 0))
    cooper_text = font.render("Cooper", True, (0, 0, 0))

    screen.blit(user_text, (user_pos[0] + big_size[0] // 2 - user_text.get_width() // 2, user_pos[1] + big_size[1] + 5))
    screen.blit(cooper_text,
                (cooper_pos[0] + big_size[0] // 2 - cooper_text.get_width() // 2, cooper_pos[1] + big_size[1] + 5))

    winner, explanation = get_winner(user_choice, cooper_choice)

    if winner == "tie":
        result_text = "It's a tie!"
        color = (0, 0, 128)
    elif winner == "user":
        result_text = f"You win! {explanation}"
        color = (0, 128, 0)
    else:
        result_text = f"Cooper wins! {explanation}"
        color = (128, 0, 0)

    result_render = font.render(result_text, True, color)
    result_pos = (WIDTH // 2 - result_render.get_width() // 2, cooper_pos[1] + big_size[1] + 40)
    screen.blit(result_render, result_pos)

    # Replay and Exit buttons
    button_width, button_height = 100, 40
    gap = 40
    total_width = button_width * 2 + gap
    start_x = WIDTH // 2 - total_width // 2
    y_buttons = result_pos[1] + 50

    # replay_button = pygame.Rect(start_x, y_buttons, button_width, button_height)
    # exit_button = pygame.Rect(start_x + button_width + gap, y_buttons, button_width, button_height)

    replay_button = pygame.Rect(200, 340, 100, 40)
    exit_button = pygame.Rect(320, 340, 100, 40)


    pygame.draw.rect(screen, (0, 200, 0), replay_button)
    pygame.draw.rect(screen, (200, 0, 0), exit_button)

        # Draw black borders around buttons
    pygame.draw.rect(screen, (0, 0, 0), replay_button, 2)
    pygame.draw.rect(screen, (0, 0, 0), exit_button, 2)

    replay_text = button_font.render("Replay", True, (255, 255, 255))
    exit_text = button_font.render("Exit", True, (255, 255, 255))

    # Fix text centering (since blit uses top-left)
    screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))

    pygame.display.flip()

    return replay_button, exit_button


def main():
    draw_main_screen()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    show_rules_popup()
                    waiting = False

    running = True
    show_sign_selection()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Check icon buttons in selection mode
                for name, rect in icon_buttons:
                    if rect.collidepoint(pos):
                        user_choice = name
                        cooper_choice = random.choice(list(sign_images.keys()))
                        replay_button, exit_button = draw_choices(user_choice, cooper_choice)

                        # Wait for Replay or Exit click
                        waiting_result = True
                        while waiting_result:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    waiting_result = False
                                    running = False
                                elif e.type == pygame.MOUSEBUTTONDOWN:
                                    if replay_button.collidepoint(e.pos):
                                        show_sign_selection()
                                        waiting_result = False
                                    elif exit_button.collidepoint(e.pos):
                                        waiting_result = False
                                        running = False
                        break

    pygame.quit()


if __name__ == "__main__":
    main()
