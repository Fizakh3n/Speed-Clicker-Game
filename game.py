import pygame  
import random  

# Initialize Pygame
pygame.init()

# Game Window
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speed Clicker Game")

# Colors
def get_gradient_color(y):
    """Generate a dynamic gradient color based on y-position."""
    r = min(255, 50 + y // 2)
    g = min(255, 30 + y // 3)
    b = min(255, 100 + y // 4)
    return (r, g, b)

WHITE = (255, 255, 255)
NAVY_BLUE = (0, 0, 128)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# Game Variables
score = 0
best_score = 0
targets = []  # Stores target circles
target_timer = 0  # Timer to track target lifespan
TARGET_LIFETIME = 5000  # 5 seconds per target

# Font
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def display_end_message():
    screen.fill(WHITE)
    message = font.render("Oops! Try Again", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    best_text = font.render(f"Best Score: {best_score}", True, BLACK)
    
    screen.blit(message, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
    screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
    screen.blit(best_text, (WIDTH // 2 - 80, HEIGHT // 2 + 40))
    
    pygame.display.update()
    pygame.time.delay(2000)

# Function to spawn a target
def spawn_target():
    global target_timer
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    radius = random.randint(15, 30)
    targets.clear()
    targets.append({"x": x, "y": y, "radius": radius})
    target_timer = pygame.time.get_ticks()

# Spawn initial target
spawn_target()

# Game Loop
running = True
while running:
    # Create gradient background
    for y in range(HEIGHT):
        pygame.draw.line(screen, get_gradient_color(y), (0, y), (WIDTH, y))
    
    # Calculate countdown timer
    time_left = max(0, TARGET_LIFETIME - (pygame.time.get_ticks() - target_timer)) // 1000
    
    if time_left == 0:
        best_score = max(best_score, score)
        display_end_message()
        running = False  # End game after message

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for target in targets[:]:  # Copy list to avoid modification issues
                dist = ((mx - target["x"])**2 + (my - target["y"])**2) ** 0.5
                if dist <= target["radius"]:  # Check if clicked inside circle
                    score += 1
                    spawn_target()  # Replace with new target

    # Draw Targets
    for target in targets:
        pygame.draw.circle(screen, GOLD, (target["x"], target["y"]), target["radius"])
        pygame.draw.circle(screen, WHITE, (target["x"], target["y"]), target["radius"] // 2)

    # Display Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display Countdown Timer
    timer_text = font.render(f"Time Left: {time_left}s", True, BLACK)
    screen.blit(timer_text, (WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(60)  # Limit frame rate

pygame.quit()

