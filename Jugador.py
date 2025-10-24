import pygame
import Configuracion as s
import UtilidadesDelMundo as world_utils

def create_player_sprite():
    """ Crea una superficie de Pygame para el sprite del jugador """
    sprite = pygame.Surface((s.TILE_SIZE - 4, s.TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(sprite, (255, 200, 150), (3, 0, s.TILE_SIZE - 10, 5))
    pygame.draw.rect(sprite, (0, 100, 200), (0, 5, s.TILE_SIZE - 4, 8))
    pygame.draw.rect(sprite, (50, 30, 0), (2, 13, s.TILE_SIZE - 8, 7))
    return sprite

class Player:
    def __init__(self, x_blocks, y_blocks):
        self.image = create_player_sprite()
        self.rect = pygame.Rect(x_blocks * s.TILE_SIZE, y_blocks * s.TILE_SIZE, self.image.get_width(), self.image.get_height())
        
        self.vx = 0.0
        self.vy = 0.0
        self.move_speed = 0.4       
        self.max_speed = 4.0        
        self.friction = 0.85        
        self.jump_power = -10.0
        self.on_ground = False
        self.facing_right = True
        
        self.clase = "Aspirante"
        self.health = 100
        self.max_health = 100
        self.hunger = 100
        self.max_hunger = 100
        self.mana = 0
        self.max_mana = 0
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.invincible = False
        self.invincibility_timer = 0
        
        self.inventory = {} 
        self.hotbar = [None] * 9 
        self.hotbar_selected = 0 
        self.inventory_open = False 
        
    def update(self, world, moving_left, moving_right):
        
        if moving_left:
            self.vx -= self.move_speed
            self.facing_right = False
        if moving_right:
            self.vx += self.move_speed
            self.facing_right = True
            
        if not moving_left and not moving_right:
            self.vx *= self.friction
            if abs(self.vx) < 0.1: self.vx = 0
            
        if self.vx > self.max_speed: self.vx = self.max_speed
        if self.vx < -self.max_speed: self.vx = -self.max_speed
            
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

    def update_invincibility(self, dt):
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False
                
    def take_damage(self, amount, notification_manager):
        if not self.invincible:
            self.health -= amount
            notification_manager.add_notification(f"Recibes {amount} de daño!", (255, 0, 0))
            self.invincible = True
            self.invincibility_timer = 1.0 
            if self.health <= 0:
                self.health = 0
                notification_manager.add_notification("¡Has muerto!", (255, 0, 0))

    def draw(self, screen, offset_x, offset_y):
        img_to_draw = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
        if self.invincible:
            if int(self.invincibility_timer * 10) % 2 == 0:
                return 
        
        screen.blit(
            img_to_draw,
            (self.rect.x - offset_x, self.rect.y - offset_y)
        )

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    def attack(self):
        pass 
        
    def get_attack_rect(self):
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.y, s.TILE_SIZE * 2, self.rect.height)
        else:
            return pygame.Rect(self.rect.left - (s.TILE_SIZE * 2), self.rect.y, s.TILE_SIZE * 2, self.rect.height)

    def add_to_inventory(self, item_name_or_id):
        item_name = s.BLOCK_NAMES.get(item_name_or_id, str(item_name_or_id))
        
        if item_name_or_id in s.RECIPES:
            item_name = item_name_or_id
            
        if not item_name: return

        self.inventory[item_name] = self.inventory.get(item_name, 0) + 1
        
        for i in range(len(self.hotbar)):
            if self.hotbar[i] and self.hotbar[i]['name'] == item_name:
                self.hotbar[i]['count'] += 1
                return
        
        for i in range(len(self.hotbar)):
            if self.hotbar[i] is None:
                item_id = None
                if isinstance(item_name_or_id, int):
                    item_id = item_name_or_id
                
                self.hotbar[i] = {'id': item_id, 'name': item_name, 'count': 1}
                return

    def get_selected_block_id(self):
        selected = self.hotbar[self.hotbar_selected]
        if selected and selected['id'] is not None:
            return selected['id']
        return None

    def use_selected_item(self):
        selected = self.hotbar[self.hotbar_selected]
        if selected:
            item_name = selected['name']
            selected['count'] -= 1
            self.inventory[item_name] -= 1 
            
            if selected['count'] <= 0:
                self.hotbar[self.hotbar_selected] = None
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
            return True
        return False

    def add_xp(self, amount):
        if self.clase == "Aspirante": return
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

    def set_clase(self, clase):
        self.clase = clase
        if clase == "Mago":
            self.max_mana = 50
            self.mana = 50
        elif clase == "Guerrero":
            self.max_health = 150
            self.health = 150
