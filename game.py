import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
DOT_RADIUS = 30
BG_COLOR = (10, 10, 30)  # Navy Blue
DOT_COLOR = (255, 215, 0)  # Golden
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER = (30, 120, 220)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Speed Click Game")

# Font
font = pygame.font.Font(None, 40)

# Initialize variables
score = 0
best_score = 0
dot_x = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS)
dot_y = random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
timer = 5000  # 5 seconds in milliseconds
start_ticks = pygame.time.get_ticks()
game_over = False
paused = False
fullscreen = False

# Button Function
def draw_button(text, x, y, w, h):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    color = BUTTON_HOVER if (x <= mouse_x <= x + w and y <= mouse_y <= y + h) else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (x + 15, y + 10))
    return x <= mouse_x <= x + w and y <= mouse_y <= y + h

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)

    # Time countdown
    if not paused and not game_over:
        time_left = timer - (pygame.time.get_ticks() - start_ticks)
        if time_left <= 0:
            game_over = True

    # Draw dot
    if not game_over and not paused:
        pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), DOT_RADIUS)

    # Display score & timer
    score_text = font.render(f"Score: {score}", True, WHITE)
    time_text = font.render(f"Time Left: {max(time_left // 1000, 0)} sec", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (20, 60))

    # Pause button
    pause_hover = draw_button("Pause" if not paused else "Resume", WIDTH - 150, 20, 120, 40)

    # Game over message
    if game_over:
        best_score = max(best_score, score)
        msg = font.render(f"Oops! Try Again. Best: {best_score}, Your Score: {score}", True, WHITE)
        screen.blit(msg, (WIDTH // 6, HEIGHT // 2))
        retry_hover = draw_button("Try Again", WIDTH // 2 - 60, HEIGHT // 2 + 50, 150, 50)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if pause_hover:  # Pause/Resume
                paused = not paused
            
            if game_over and retry_hover:  # Restart game
                score = 0
                dot_x = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS)
                dot_y = random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
                start_ticks = pygame.time.get_ticks()
                game_over = False

            if not game_over and not paused:
                if (dot_x - mouse_x) ** 2 + (dot_y - mouse_y) ** 2 <= DOT_RADIUS ** 2:
                    score += 1
                    dot_x = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS)
                    dot_y = random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
                    start_ticks = pygame.time.get_ticks()  # Reset timer

    pygame.display.flip()

pygame.quit()



