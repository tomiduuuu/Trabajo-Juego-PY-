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
        
        # Física mejorada (estilo Terraria)
        self.vx = 0.0
        self.vy = 0.0
        self.move_speed = 8.0        # Más rápido
        self.acceleration = 0.5      # Aceleración suave
        self.deceleration = 0.4      # Desaceleración suave
        self.max_speed = 8.0        
        self.jump_power = -12.0      # Salto más potente
        self.on_ground = False
        self.facing_right = True
        
        # Estadísticas del jugador
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
        
        # Inventario y equipo
        self.inventory = {} 
        self.hotbar = [None] * 9 
        self.hotbar_selected = 0 
        self.inventory_open = False
        self.equipped_tool = None
        self.equipped_weapon = None
        
        # Sistema de minería progresiva
        self.mining_target = None  # (x, y) del bloque que se está minando
        self.mining_progress = 0.0  # Progreso actual (0.0 a 1.0)
        self.mining_speed = 1.0     # Velocidad base (mano)
        
    def update(self, world, moving_left, moving_right):
        # Movimiento horizontal mejorado (estilo Terraria)
        if moving_left:
            if self.vx > 0:  # Cambiando de dirección
                self.vx -= self.deceleration * 2
            else:
                self.vx -= self.acceleration
            self.facing_right = False
            
        if moving_right:
            if self.vx < 0:  # Cambiando de dirección
                self.vx += self.deceleration * 2
            else:
                self.vx += self.acceleration
            self.facing_right = True
            
        # Desaceleración cuando no se mueve
        if not moving_left and not moving_right:
            if self.vx > 0:
                self.vx -= self.deceleration
                if self.vx < 0: self.vx = 0
            elif self.vx < 0:
                self.vx += self.deceleration
                if self.vx > 0: self.vx = 0
        
        # Limitar velocidad máxima
        if self.vx > self.max_speed: self.vx = self.max_speed
        if self.vx < -self.max_speed: self.vx = -self.max_speed
            
        # Aplicar movimiento horizontal
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
        
        # Aplicar gravedad
        if not self.on_ground:
            self.vy += s.GRAVITY
            if self.vy > 15: self.vy = 15  # Velocidad terminal más alta
                
        self.rect.y += int(self.vy)
        self.on_ground = False 
        
        # Colisión vertical
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

    def update_mining(self, dt, world, target_block):
        """Actualiza el progreso de minería"""
        if target_block != self.mining_target:
            # Cambió el bloque objetivo, reiniciar progreso
            self.mining_target = target_block
            self.mining_progress = 0.0
            return False
        
        if target_block is None:
            self.mining_progress = 0.0
            return False
            
        gx, gy = target_block
        block_id = world_utils.get_block(world, gx, gy)
        
        if block_id == s.BLOCK_AIR:
            # El bloque ya fue minado
            self.mining_progress = 0.0
            self.mining_target = None
            return False
        
        # Calcular velocidad de minería
        mining_speed = self.get_mining_speed(block_id)
        base_time = s.BLOCK_HARDNESS.get(block_id, 3.0)
        time_to_mine = base_time / mining_speed
        
        # Actualizar progreso
        self.mining_progress += dt / time_to_mine
        
        if self.mining_progress >= 1.0:
            # Bloque minado completamente
            self.mining_progress = 0.0
            self.mining_target = None
            return True
        
        return False

    def get_mining_speed(self, block_id):
        """Obtiene la velocidad de minería para un bloque específico"""
        # Velocidad base (mano)
        speed = s.TOOL_SPEED["Mano"]
        
        # Verificar herramienta equipada
        selected = self.hotbar[self.hotbar_selected]
        if selected:
            tool_name = selected['name']
            if tool_name in s.TOOL_SPEED:
                # Verificar si la herramienta es efectiva para este bloque
                if self.is_tool_effective(tool_name, block_id):
                    speed = s.TOOL_SPEED[tool_name]
                else:
                    # Herramienta no efectiva, penalización
                    speed = max(1.0, s.TOOL_SPEED[tool_name] * 0.3)
        
        return speed

    def is_tool_effective(self, tool_name, block_id):
        """Verifica si la herramienta es efectiva para el bloque"""
        if block_id not in s.EFFECTIVE_TOOLS:
            return True  # Bloques sin herramienta específica
        
        effective_tools = s.EFFECTIVE_TOOLS[block_id]
        tool_type = self.get_tool_type(tool_name)
        
        return tool_type in effective_tools

    def get_tool_type(self, tool_name):
        """Obtiene el tipo de herramienta"""
        if "pico" in tool_name.lower():
            return "pico"
        elif "pala" in tool_name.lower():
            return "pala"
        elif "hacha" in tool_name.lower():
            return "hacha"
        return "mano"

    def get_mining_progress(self):
        """Obtiene el progreso actual de minería (0.0 a 1.0)"""
        return self.mining_progress

    def stop_mining(self):
        """Detiene la minería actual"""
        self.mining_progress = 0.0
        self.mining_target = None

    def get_mining_info(self):
        """Obtiene información sobre la minería actual"""
        return self.mining_target, self.mining_progress

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
        """Dibuja al jugador en la pantalla"""
        img_to_draw = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        
        if self.invincible:
            if int(self.invincibility_timer * 10) % 2 == 0:
                return  # Efecto de parpadeo cuando es invencible
        
        screen.blit(
            img_to_draw,
            (self.rect.x - offset_x, self.rect.y - offset_y)
        )

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    def attack(self):
        # Verificar si tiene un arma equipada
        selected = self.hotbar[self.hotbar_selected]
        if selected and "Espada" in selected['name']:
            self.equipped_weapon = selected['name']
            return True
        return False
        
    def get_attack_rect(self):
        attack_range = s.TILE_SIZE * 1.5
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.y, attack_range, self.rect.height)
        else:
            return pygame.Rect(self.rect.left - attack_range, self.rect.y, attack_range, self.rect.height)

    def add_to_inventory(self, item_name_or_id):
        item_name = s.BLOCK_NAMES.get(item_name_or_id, str(item_name_or_id))
        
        if item_name_or_id in s.RECIPES:
            item_name = item_name_or_id
            
        if not item_name: return

        self.inventory[item_name] = self.inventory.get(item_name, 0) + 1
        
        # Actualizar hotbar
        for i in range(len(self.hotbar)):
            if self.hotbar[i] and self.hotbar[i]['name'] == item_name:
                self.hotbar[i]['count'] += 1
                return
        
        # Agregar a slot vacío
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
            self.max_mana = 100
            self.mana = 100
        elif clase == "Guerrero":
            self.max_health = 150
            self.health = 150
        elif clase == "Arquero":
            self.max_health = 120
            self.health = 120