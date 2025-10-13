from random import randint

import pygame.draw
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # GROUPS
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # SPRITES
        self.player = Player((500, 300), self.all_sprites, self.collision_sprites)
    def setup(self):
        map = load_pygame('S:\\Vscode\\aBUBU\\VampireSurvivorsPyGAME\\Vampire survivor\\data\\maps\\world.tmx')
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:
            dt = self.clock.tick(200) / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)
            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.draw.rect(self.display_surface, 'red', self.player.hitbox_rect)
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()