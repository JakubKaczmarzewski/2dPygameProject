import pygame
import pygame as pg
import random
from settings import *
from sprites import *
import time

left = -5
right = 5
max_height = height
Highest_location = vec(200, height)
move_counter = 0
sequences = []
sequence = []
end = True
jump_chanse = 0.25

class Game:
    def __init__(self):
        # Preparing libraries and creating a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        # Storing object movement sequences
        self.sequence =[]

    def new(self):
        # Starting a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        global end
        global move_counter
        global Highest_location
        global max_height
        global sequences
        global sequence
        global left
        global right

        # Updating
        self.all_sprites.update()

        # Collision with objects
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if  end:
            if self.player.pos.y >= height - 750 and end:
                self.losowy_ruch()
                self.czy_wyzej()
            if pg.sprite.spritecollide(self.player, self.platforms, False) and self.player.pos.y <= height - 750:
                end = False
                self.player.vel.x = 0
                self.player.vel.y = 0
                self.player.pos = vec(200, height)
                left = 0
                right = 0
                Highest_location = (200, height)
            move_counter = move_counter % 50

            if move_counter == 49 and end:
                self.player.pos = Highest_location
                sequence = []
            #pg.time.wait(500)
            move_counter += 1

    def events(self):
        # game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # game loop - draw
        # Render
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def losowy_ruch(self):
        global sequence
        global left
        global right
        # Random move
        ruch = random.choice([left, right])
        self.player.vel.x = ruch * player_speed
        if random.random() <= jump_chanse:
            self.player.jump()
            # Saving jump sequence to an array
            sequence.append(('skok', self.player.vel.x))
        else:
            sequence.append(('ruch', self.player.vel.x))




    def czy_wyzej(self):
        global max_height
        global Highest_location
        global sequences
        global sequence
        if (self.player.rect.bottom < max_height) and (len(pg.sprite.spritecollide(self.player, self.platforms, False)) > 0) and self.player.vel.y >= 0:
            max_height = self.player.rect.bottom
            Highest_location = (self.player.pos.x , self.player.pos.y)
            sequences.append(sequence)
            print(Highest_location)
            print(sequence)
            return True

        return False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()

# Game loop
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()