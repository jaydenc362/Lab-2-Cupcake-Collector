import pygame
import random
import asyncio

# Initialize
pygame.init()
WIDTH = 640
HEIGHT = 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jayden Chan Period 5: Lab 2 Cupcake Collector")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
running = True
dt = 0

# Setup
score = 0
cupcakeSpawns = 5

# Sprites
playerSprite = pygame.image.load("player.png").convert_alpha()
cupcakeSprite = pygame.image.load("cupcake.png").convert_alpha()

class Player:
    def __init__(self):
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 1000
        self.size = 50
        self.sprite = playerSprite
        self.acceleration = 400
        self.jumpPower = 400
        self.isJumping = False
        self.canJump = False
    def isPlatformCollision(self, platform):
        return (
            self.position.x < platform.position.x + platform.w
            and self.position.x + self.size > platform.position.x
            and self.position.y < platform.position.y + platform.h
            and self.position.y + self.size > platform.position.y
        )
    def doPlatformCollision(self, platform, oldX, oldY):
        if oldY + self.size <= platform.position.y:
            self.position.y = platform.position.y - self.size
            self.velocity.y = 0
            self.canJump = True
            self.isJumping = False
        elif oldY >= platform.position.y + platform.h:
            self.position.y = platform.position.y + platform.h
            self.velocity.y = 0
        elif oldX + self.size <= platform.position.x:
            self.position.x = platform.position.x - self.size
            self.velocity.x = 0
        elif oldX >= platform.position.x + platform.w:
            self.position.x = platform.position.x + platform.w
            self.velocity.x = 0
    def doWallCollision(self):
        if self.position.x < 0:
            self.velocity.x = 0
            self.position.x = 0
        elif self.position.x > WIDTH - self.size:
            self.velocity.x = 0
            self.position.x = WIDTH - self.size
        if self.position.y < 0:
            self.velocity.y = 0
            self.position.y = 0
        elif self.position.y > HEIGHT - self.size:
            self.velocity.y = 0
            self.position.y = HEIGHT - self.size
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        # X Control
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.velocity.x -= self.acceleration * dt
            if self.velocity.x < -self.acceleration:
                self.velocity.x = -self.acceleration
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.velocity.x += self.acceleration * dt
            if self.velocity.x > self.acceleration:
                self.velocity.x = self.acceleration
        else:
            if self.velocity.x > 0: self.velocity.x -= self.acceleration * dt
            elif self.velocity.x < 0: self.velocity.x += self.acceleration * dt
        # Y Control
        if not keys[pygame.K_UP]: self.isJumping = False
        if keys[pygame.K_UP] and self.canJump and not self.isJumping:
            self.velocity.y = -self.jumpPower
            self.isJumping = True
        # Physics
        oldX = self.position.x
        oldY = self.position.y
        self.position.x += self.velocity.x * dt
        self.velocity.y += self.gravity * dt
        self.position.y += self.velocity.y * dt
        self.doWallCollision()
        # Platforms
        self.canJump = False
        for platform in platforms:
            if self.isPlatformCollision(platform):
                self.doPlatformCollision(
                    platform, oldX, oldY
                )
    def draw(self, screen):
        image = pygame.transform.scale(self.sprite, (self.size, self.size))
        screen.blit(image, (self.position.x, self.position.y))

class Platform:
    def __init__(self, x, y, w, h):
        self.position = pygame.Vector2(x, y)
        self.w, self.h = w, h
        self.color = "dodgerblue4"
    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color,
            (self.position.x, self.position.y,
            self.w, self.h)
        )

class Cupcake:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.size = 50
        self.sprite = cupcakeSprite
    def isPlayerCollision(self, player):
        return (
            self.position.x < player.position.x + player.size
            and self.position.x + self.size > player.position.x
            and self.position.y < player.position.y + player.size
            and self.position.y + self.size > player.position.y
        )
    def recycle(self, cupcakes):
        cupcakes.remove(self)
        cupcakes.append(
            Cupcake(
                random.randint(50, WIDTH - 100),
                random.randint(50, HEIGHT - 100)
            )
        )
    def draw(self, screen):
        image = pygame.transform.scale(self.sprite, (self.size, self.size))
        screen.blit(image, (self.position.x, self.position.y))

# Create Player
player = Player()

# Create Platforms
platforms = []
platforms.append(Platform(0, HEIGHT - 50, WIDTH, 50))
platforms.append(Platform(20, 220, 200, 30))
platforms.append(Platform(400, 250, 50, 70))
platforms.append(Platform(400, 110, 50, 50))
platforms.append(Platform(390, 150, 10, 10))
platforms.append(Platform(WIDTH - 20, 100, 60, 20))
platforms.append(Platform(WIDTH - 60, 180, 60, 20))
platforms.append(Platform(50, 70, 140, 20))
platforms.append(Platform(50, 70, 30, 50))

# Create Cupcakes
cupcakes = []
for i in range(cupcakeSpawns):
    cupcakes.append(
        Cupcake(
            random.randint(50, WIDTH - 100),
            random.randint(50, HEIGHT - 100)
        )
    )

# Game Loop
async def main():
    # Use Global Variables
    global dt, score, running
    while running:
        # Calculate dt
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update Player
        player.update(platforms)
        # Update All Cupcakes
        for cupcake in cupcakes[:]:
            if cupcake.isPlayerCollision(player):
                cupcake.recycle(cupcakes)
                score += 1
        # Draw Background
        screen.fill("cornflowerblue")
        # Draw Player
        player.draw(screen)
        # Draw All Platforms
        for platform in platforms:
            platform.draw(screen)
        # Draw All Cupcakes
        for cupcake in cupcakes:
            cupcake.draw(screen)
        # Draw Text
        textSurface = font.render("Score: " + str(score), True, "white")
        screen.blit(textSurface, (10, 10))
        # Render
        pygame.display.flip()
        await asyncio.sleep(0)

# Run Game Loop
asyncio.run(main())
