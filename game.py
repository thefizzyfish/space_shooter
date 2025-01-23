import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen in full screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")

# Load and resize images
player_image = pygame.image.load("space_shooter/player.png")
enemy_image = pygame.image.load("space_shooter/enemy.png")
bullet_image = pygame.image.load("space_shooter/bullet.png")

# Resize images to fit the screen
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (10, 20))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.base_speed = random.randint(1, 3)
        self.speed = self.base_speed 
        self.direction = random.choice([-1, 1])  # Random initial direction for x-axis movement

    def update(self, timer):
        self.rect.y += self.speed
        self.rect.x += self.direction * self.base_speed

        # Change direction if hitting screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

        # Reset position if off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.base_speed = random.randint(1, 3)
            self.speed = self.base_speed + timer // 10
            self.direction = random.choice([-1, 1])

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create initial enemies
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop
running = True
game_over = False
start_ticks = pygame.time.get_ticks()  # Get the initial tick count
score = 0
font = pygame.font.Font(None, 36)
score_text = font.render("Score: " + str(score), True, WHITE)
last_enemy_add_time = 0  # Track the last time enemies were added

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    if not game_over:
        # Update
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert milliseconds to seconds
        all_sprites.update(elapsed_time)

        # Check for collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            # update scoreboard
            score_text = font.render("Score: " + str(score), True, WHITE)

            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Add new enemies every 10 seconds
        if elapsed_time - last_enemy_add_time >= 10:
            for _ in range(5):  # Add 5 new enemies every 10 seconds
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            last_enemy_add_time = elapsed_time

        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    screen.blit(score_text, (10, 10))

    # Calculate and display the game timer
    timer_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
    screen.blit(timer_text, (10, 40))

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
        running = False

    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()