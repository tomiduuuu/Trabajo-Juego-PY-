import pygame
import Configuracion as s
import UtilidadesDelMundo as world_utils

class Zombie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, s.TILE_SIZE - 4, s.TILE_SIZE)
        self.color = (50, 150, 50) # Verde zombie
        
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.move_speed = 1.0 
        self.facing_right = True
        
        self.health = 50
        self.aggro_range = s.TILE_SIZE * 10 
        self.state = "patrolling" 

    def update(self, world, player_rect):
        
        distance_to_player = abs(player_rect.centerx - self.rect.centerx)
        
        if distance_to_player < self.aggro_range:
            self.state = "chasing"
        else:
            self.state = "patrolling"
            
        if self.state == "chasing":
            if player_rect.centerx > self.rect.centerx:
                self.vx = self.move_speed
                self.facing_right = True
            else:
                self.vx = -self.move_speed
                self.facing_right = False
        else:
            self.vx = 0 

        self.rect.x += int(self.vx)
        colliding_blocks = world_utils.get_blocks_in_rect(world, self.rect)
        for x, y in colliding_blocks:
            block_rect = pygame.Rect(x * s.TILE_SIZE, y * s.TILE_SIZE, s.TILE_SIZE, s.TILE_SIZE)
            if self.vx > 0: 
                self.rect.right = block_rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block_rect.right
                self.vx = 0
        
        if not self.on_ground:
            self.vy += s.GRAVITY
            if self.vy > 10: self.vy = 10
                
        self.rect.y += int(self.vy)
        self.on_ground = False 
        
        colliding_blocks = world_utils.get_blocks_in_rect(world, self.rect)
        for x, y in colliding_blocks:
            block_rect = pygame.Rect(x * s.TILE_SIZE, y * s.TILE_SIZE, s.TILE_SIZE, s.TILE_SIZE)
            if self.vy > 0:
                self.rect.bottom = block_rect.top
                self.on_ground = True
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block_rect.bottom
                self.vy = 0

    def take_damage(self, player, amount):
        self.health -= amount
        if player.facing_right:
            self.vx = 5
        else:
            self.vx = -5
        self.vy = -3 
        self.on_ground = False

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(
            screen, self.color,
            (self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height)
        )
        if self.health < 50:
            health_rect_bg = pygame.Rect(self.rect.x - offset_x, self.rect.y - offset_y - 8, self.rect.width, 5)
            health_rect_fg = pygame.Rect(self.rect.x - offset_x, self.rect.y - offset_y - 8, int(self.rect.width * (self.health / 50)), 5)
            pygame.draw.rect(screen, (255, 0, 0), health_rect_bg)
            pygame.draw.rect(screen, (0, 255, 0), health_rect_fg)
