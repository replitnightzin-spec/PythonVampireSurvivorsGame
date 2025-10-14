import pygame.mouse
from math import atan2, degrees

from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player conection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)

        # sprites
        super().__init__(groups)
        self.gun_surface = pygame.image.load('S:\\Vscode\\aBUBU\VampireSurvivorsPyGAME\\Vampire survivor\\images\\gun\\gun.png')
        self.image = self.gun_surface
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surface, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surface, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.spawn_timer = pygame.time.get_ticks()
        self.lifetime = 1000

        self.direction = direction
        self.speed = 1200
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_timer >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        # image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        # rect
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350


    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, dt):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        # update the rect position + collision
        self.hitbox.centerx += self.direction.x  * self.speed * dt
        self.collisions('horizontal')
        self.hitbox.centery += self.direction.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitbox.center
    def collisions(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top



    def update(self, dt):
        self.move(dt)
        self.animate(dt)
