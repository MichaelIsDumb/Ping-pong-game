import pygame
from pygame import sprite, transform, image, key, display, font, mixer, event
from pygame.locals import *
from random import randint, uniform

# Initialize Pygame
pygame.init()

window = display.set_mode((700, 500))
display.set_caption('Ping pong')

# Colors
blue = (0, 191, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Score
A_point = 0
B_point = 0

# Class for game sprites
class GameSprite(sprite.Sprite):
    def __init__(self, object_image, object_width, object_height, object_x, object_y, object_speed, other_speed):
        super().__init__()
        self.image = transform.scale(image.load(object_image), (object_width, object_height))
        self.rect = self.image.get_rect()
        self.rect.x = object_x
        self.rect.y = object_y
        self.speed = object_speed
        self.otherspeed = other_speed

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def control(self, up_key, down_key):
        keys_pressed = key.get_pressed()
        if keys_pressed[up_key] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[down_key] and self.rect.y < 410:  # Adjusted boundary for player movement
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, object_image, object_width, object_height, object_x, object_y, object_speed, other_speed):
        super().__init__(object_image, object_width, object_height, object_x, object_y, object_speed, other_speed)
        self.direction_x = 1 if randint(0, 1) == 0 else -1

    def movement(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.otherspeed

    def collide(self, Player):
        if sprite.collide_rect(Player, self):
            self.direction_x *= -1
            self.speed *= uniform(1, 1.05)
            self.otherspeed *= uniform(1, 1.05)

    def collide_wall(self):
        if self.rect.y >= 460 or self.rect.y <= 0:
            self.otherspeed = -self.otherspeed * uniform(1, 1.05)

    def reset_position(self):
        global A_point, B_point
        if self.rect.x <= 0:
            self.rect.x, self.rect.y = 325, 230
            self.speed, self.otherspeed = 3, 3
            B_point += 1
            self.direction_x = 1  # Reset direction
        elif self.rect.x >= 660:
            self.rect.x, self.rect.y = 325, 230
            self.speed, self.otherspeed = 3, 3
            A_point += 1
            self.direction_x = -1  # Reset direction

# Font
font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 70)

# Music
mixer.init()

# Variables for restart function
play_again = font1.render('Type [R] to play again', True, red)
quit_game = font1.render('Type [X] to close the window', True, red)
ready = font1.render("Are you ready? Type [yes]", True, red)

# Main game function
def main_game():
    global A_point, B_point
    game_status = True
    clock = pygame.time.Clock()
    finish = False

    window = display.set_mode((700, 500))
    display.set_caption('Ping pong')
    background = transform.scale(image.load('kurzgesagt.jpeg'), (700, 500))

    # Create players
    Sprite_1 = Player('duck1.png', 90, 90, 1, 205, 5, None)
    Sprite_2 = Player('duck2.png', 90, 90, 610, 205, 5, None)
    Pingball = Ball('pingball.png', 40, 40, 325, 230, 3, 3)

    # Game texture
    your_display = font1.render('You', True, (255, 255, 255))
    opponent_display = font1.render('Opponent', True, (255, 255, 255))
    getting_out = font1.render('Press [R] to leave', True, (255, 255, 255))
    win = font2.render('YOU WIN', True, (255, 0, 0))
    lose = font2.render('YOU LOSE', True, (255, 0, 0))

    # Music
    mixer.music.load('Seemefall.mp3') #doesn't work right now, there is some copyright issue with the music
    mixer.music.play()

    # Running loop
    while game_status:
        for e in event.get():
            if e.type == QUIT:
                game_status = False
            if e.type == KEYDOWN and e.key == K_r:
                game_status = False

        if not finish:
            window.blit(background, (0, 0))
            # Setup
            Sprite_1.show()
            Sprite_1.control(K_w, K_s)
            Sprite_2.show()
            Sprite_2.control(K_UP, K_DOWN)
            Pingball.show()

            # Controls
            Pingball.movement()
            Pingball.collide(Sprite_1)
            Pingball.collide(Sprite_2)
            Pingball.collide_wall()
            Pingball.reset_position()

            player_1 = font1.render(str(A_point), True, (255, 255, 255))
            player_2 = font1.render(str(B_point), True, (255, 255, 255))

            # Winning and losing condition
            if A_point == 5:
                window.blit(win, (250, 235))
                window.blit(getting_out, (350, 450))
                finish = True
            elif B_point == 5:
                window.blit(lose, (250, 235))
                window.blit(getting_out, (350, 450))
                finish = True

            window.blit(your_display, (20, 5))
            window.blit(opponent_display, (590, 5))
            window.blit(player_1, (45, 40))
            window.blit(player_2, (655, 40))

        display.update()
        clock.tick(60)

def restart():
    mixer.music.stop()
    clock = pygame.time.Clock()
    window.fill(black)
    window.blit(play_again, (245, 200))
    window.blit(quit_game, (215, 300))
    display.update()
    clock.tick(60)
    user_box = input('')
    return user_box.upper() == 'R'

def intro():
    mixer.music.stop()
    clock = pygame.time.Clock()
    window.fill(black)
    window.blit(ready, (235, 240))
    display.update()
    clock.tick(60)

def start_game():
    global A_point, B_point
    running = True
    while running:
        intro()
        answer = input('').strip().lower()
        if answer == 'yes':
            main_game()
            A_point, B_point = 0, 0
            if not restart():
                running = False
        else:
            running = False

start_game()
pygame.quit()
