import pygame
import math
import Configuracion as s

# --- Funciones de Interacción y Dibujado del Mundo ---

def get_block(world, x, y):
    """ Obtiene un bloque de las coordenadas del mundo (en bloques) """
    if 0 <= x < s.WORLD_WIDTH and 0 <= y < s.WORLD_HEIGHT:
        return world[x][y]
    return s.BLOCK_AIR # Fuera del mundo es aire

def get_blocks_in_rect(world, rect):
    """ Devuelve los bloques (x, y) que colisionan con un rect (en pixeles) """
    blocks = []
    x1 = max(0, rect.left // s.TILE_SIZE)
    y1 = max(0, rect.top // s.TILE_SIZE)
    x2 = min(s.WORLD_WIDTH - 1, rect.right // s.TILE_SIZE)
    y2 = min(s.WORLD_HEIGHT - 1, rect.bottom // s.TILE_SIZE)
    
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if get_block(world, x, y) != s.BLOCK_AIR:
                blocks.append((x, y))
    return blocks

def draw_world(screen, world, offset_x, offset_y):
    start_x = max(0, offset_x // s.TILE_SIZE)
    end_x = min(s.WORLD_WIDTH, (offset_x + s.WIDTH) // s.TILE_SIZE + 2)
    start_y = max(0, offset_y // s.TILE_SIZE)
    end_y = min(s.WORLD_HEIGHT, (offset_y + s.HEIGHT) // s.TILE_SIZE + 2)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            block = get_block(world, x, y)
            if block != s.BLOCK_AIR:
                color = s.COLORS.get(block, (255, 0, 255)) 
                rect = pygame.Rect(
                    x * s.TILE_SIZE - offset_x,
                    y * s.TILE_SIZE - offset_y,
                    s.TILE_SIZE, s.TILE_SIZE
                )
                pygame.draw.rect(screen, color, rect)

def modify_block(world, player, gx, gy, new_block_id, notification_manager):
    player_gx = player.rect.centerx // s.TILE_SIZE
    player_gy = player.rect.centery // s.TILE_SIZE
    
    distance = math.sqrt((player_gx - gx)**2 + (player_gy - gy)**2)
    
    if distance > s.PLAYER_REACH:
        notification_manager.add_notification("Demasiado lejos")
        return 

    if 0 <= gx < s.WORLD_WIDTH and 0 <= gy < s.WORLD_HEIGHT:
        if new_block_id == s.BLOCK_AIR: # Destruir
            existing_block = world[gx][gy]
            if existing_block != s.BLOCK_AIR:
                world[gx][gy] = s.BLOCK_AIR
                player.add_to_inventory(existing_block)
                # XP
                xp_gain = 5
                if existing_block == s.BLOCK_DIAMOND_ORE: xp_gain = 100
                elif existing_block == s.BLOCK_GOLD_ORE: xp_gain = 40
                elif existing_block == s.BLOCK_IRON_ORE: xp_gain = 20
                player.add_xp(xp_gain)
        else: # Colocar
            player_rect_blocks = player.rect.inflate(-4, -4).move(-player.rect.x, -player.rect.y)
            player_rect_blocks.move_ip(player.rect.x // s.TILE_SIZE, player.rect.y // s.TILE_SIZE)
            
            if gx == player_rect_blocks.x and (gy == player_rect_blocks.y or gy == player_rect_blocks.bottom):
                 notification_manager.add_notification("No puedes colocar un bloque aquí")
                 return 

            if player.use_selected_item(): 
                world[gx][gy] = new_block_id
            else:
                notification_manager.add_notification("No tienes ese bloque")
