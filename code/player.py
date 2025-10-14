import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.image = pygame.image.load('S:\\Vscode\\aBUBU\\VampireSurvivorsPyGAME\\Vampire survivor\\images\player\\down\\0.png').convert_alpha()
        self.state, self.frame_index = 'down', 0
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,-60)
        self.health = 100

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {'left':[],'right':[],'up':[],'down':[],}


        for state in self.frames.keys():
            for folder_path, sub_folder, file_names in walk(join('S:\\Vscode\\aBUBU\\VampireSurvivorsPyGAME\\Vampire survivor\\images\\player', state)):
               if file_names:
                   for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                       full_path = join(folder_path, file_name)
                       surf = pygame.image.load(full_path).convert_alpha()
                       self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        # MOVIMENTO HORIZONTAL
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.horizontal_collision()

        # MOVIMENTO VERTICAL
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.vertical_collision()

        # Sincronizar o rect do sprite com a hitbox
        self.rect.center = self.hitbox_rect.center

    def horizontal_collision(self):
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if self.direction.x > 0:  # movendo para direita
                    overlap = self.hitbox_rect.right - sprite.rect.left
                    self.hitbox_rect.right -= overlap
                elif self.direction.x < 0:  # movendo para esquerda
                    overlap = sprite.rect.right - self.hitbox_rect.left
                    self.hitbox_rect.left += overlap

    def vertical_collision(self):
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if self.direction.y > 0:  # movendo para baixo
                    overlap = self.hitbox_rect.bottom - sprite.rect.top
                    self.hitbox_rect.bottom -= overlap
                elif self.direction.y < 0:  # movendo para cima
                    overlap = sprite.rect.bottom - self.hitbox_rect.top
                    self.hitbox_rect.top += overlap

    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'


        # get animate
        self.frame_index += 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)