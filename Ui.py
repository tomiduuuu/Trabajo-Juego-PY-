import pygame
import Configuracion as s

# --- Sistema de Notificaciones ---
class NotificationManager:
    def __init__(self, font):
        self.notifications = [] # Lista de {'text', 'timer', 'color'}
        self.font = font
        self.max_time = 3 * 60 # 3 segundos en frames

    def add_notification(self, text, color=(255, 255, 255)):
        self.notifications.append({'text': text, 'timer': self.max_time, 'color': color})
        if len(self.notifications) > 5:
            self.notifications.pop(0)

    def draw(self, screen):
        y_pos = 10
        for i in range(len(self.notifications) - 1, -1, -1):
            notif = self.notifications[i]
            
            alpha = 255
            if notif['timer'] < 60: 
                alpha = int((notif['timer'] / 60) * 255)
            
            text_surf = self.font.render(notif['text'], True, notif['color'])
            text_surf.set_alpha(alpha)
            
            x_pos = (s.WIDTH - text_surf.get_width()) // 2
            screen.blit(text_surf, (x_pos, y_pos))
            
            y_pos += 25
            
            notif['timer'] -= 1
            if notif['timer'] <= 0:
                self.notifications.pop(i)

class TooltipManager:
    def __init__(self, font):
        self.font = font
        self.current_tooltip = None
        self.small_font = pygame.font.SysFont(None, 20)  # Fuente más pequeña
        
    def set_tooltip(self, text):
        self.current_tooltip = text
        
    def clear_tooltip(self):
        self.current_tooltip = None
        
    def draw(self, screen, is_inventory_open=False):
        if self.current_tooltip:
            mx, my = pygame.mouse.get_pos()
            
            # Usar fuente pequeña cuando NO está en inventario
            font_to_use = self.font if is_inventory_open else self.small_font
            text_surf = font_to_use.render(self.current_tooltip, True, (255, 255, 255))
            
            padding = 3 if not is_inventory_open else 5  # Menos padding cuando es pequeño
            
            bg_rect = pygame.Rect(
                mx + 10, my + 10,
                text_surf.get_width() + padding * 2,
                text_surf.get_height() + padding * 2
            )
            
            # Dibujar fondo
            pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)
            
            # Dibujar texto
            screen.blit(text_surf, (bg_rect.x + padding, bg_rect.y + padding))

# --- UI de Crafteo Clicable ---
class CraftingUI:
    def __init__(self, recipes, font, notification_manager):
        self.recipes = recipes
        self.font = font
        self.notification_manager = notification_manager
        
        self.recipe_rects = {} 
        y_pos = 180
        x_pos = 100
        for recipe_name in recipes.keys():
            self.recipe_rects[recipe_name] = pygame.Rect(x_pos, y_pos, 250, 30)
            y_pos += 35
            
    def draw(self, screen, player, tooltip_manager):
        y_pos = 180
        mx, my = pygame.mouse.get_pos()
        
        for recipe_name, rect in self.recipe_rects.items():
            can_craft = True
            recipe = s.RECIPES[recipe_name]
            
            # Verificar materiales
            missing_materials = []
            for material, amount in recipe["materials"].items():
                if player.inventory.get(material, 0) < amount:
                    can_craft = False
                    missing_materials.append(f"{material}: {player.inventory.get(material, 0)}/{amount}")
            
            color = (0, 150, 0) if can_craft else (150, 0, 0)
            pygame.draw.rect(screen, color, rect)
            
            text = f"{recipe_name} ({recipe['count']}x)"
            text_surf = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 7))
            
            # Tooltip al pasar el mouse
            if rect.collidepoint(mx, my):
                tooltip_text = f"Receta: {recipe_name}\n"
                tooltip_text += f"Produce: {recipe['count']}x\n\n"
                tooltip_text += "Materiales necesarios:\n"
                for material, amount in recipe["materials"].items():
                    has_amount = player.inventory.get(material, 0)
                    status = "✓" if has_amount >= amount else "✗"
                    tooltip_text += f"{status} {material}: {has_amount}/{amount}\n"
                
                if missing_materials:
                    tooltip_text += f"\nFaltan: {', '.join(missing_materials)}"
                
                tooltip_manager.set_tooltip(tooltip_text)
            
            y_pos += 35
            
    def check_click(self, mx, my, player):
        for recipe_name, rect in self.recipe_rects.items():
            if rect.collidepoint(mx, my):
                return recipe_name 
        return None

# --- Sistema de Crafteo (Lógica) ---
def craft_item(player, item_name, notification_manager):
    if item_name not in s.RECIPES:
        notification_manager.add_notification(f"La receta '{item_name}' no existe.", (255,0,0))
        return
        
    recipe = s.RECIPES[item_name]
    can_craft = True
    
    for material, amount in recipe["materials"].items():
        if player.inventory.get(material, 0) < amount:
            can_craft = False
            notification_manager.add_notification(f"Faltan {amount} de {material}", (255,100,0))
            break
            
    if can_craft:
        for material, amount in recipe["materials"].items():
            player.inventory[material] -= amount
            if player.inventory[material] <= 0:
                del player.inventory[material]
        
        result_name = recipe["result"]
        result_count = recipe["count"]
        
        player.inventory[result_name] = player.inventory.get(result_name, 0) + result_count
        notification_manager.add_notification(f"¡Has crafteado {result_count} x '{result_name}'!", (0,255,0))
        
        player.add_to_inventory(result_name) 
        
        # XP por crafteo
        if player.clase == "Alquimista" and "Poción" in result_name:
            player.add_xp(150)
        elif player.clase == "Alquimista":
            player.add_xp(50)
        elif "Espada" in result_name or "Arco" in result_name:
            player.add_xp(75)
        else:
            player.add_xp(30)

# --- Funciones de Dibujado de UI ---

def draw_mining_progress(screen, player, offset_x, offset_y):
    """Dibuja la barra de progreso de minería"""
    if player.mining_target and player.mining_progress > 0:
        gx, gy = player.mining_target
        block_rect = pygame.Rect(
            gx * s.TILE_SIZE - offset_x,
            gy * s.TILE_SIZE - offset_y,
            s.TILE_SIZE, s.TILE_SIZE
        )
        
        # Barra de progreso más visible
        progress_width = int(s.TILE_SIZE * player.mining_progress)
        progress_bg = pygame.Rect(block_rect.x, block_rect.y - 10, s.TILE_SIZE, 6)
        progress_fg = pygame.Rect(block_rect.x, block_rect.y - 10, progress_width, 6)
        
        pygame.draw.rect(screen, (50, 50, 50), progress_bg)
        pygame.draw.rect(screen, (255, 255, 0), progress_fg)
        pygame.draw.rect(screen, (200, 200, 200), progress_bg, 1)

def draw_hud(screen, player, font, tooltip_manager):
    # Barra de salud
    pygame.draw.rect(screen, (50, 0, 0), (10, 10, 200, 20))
    health_width = (player.health / player.max_health) * 200
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_width, 20))
    health_text = font.render(f"Vida: {player.health}/{player.max_health}", True, (255, 255, 255))
    screen.blit(health_text, (15, 12))
    
    # Barra de maná (si aplica)
    if player.max_mana > 0:
        pygame.draw.rect(screen, (0, 0, 50), (10, 35, 200, 20))
        mana_width = (player.mana / player.max_mana) * 200
        pygame.draw.rect(screen, (0, 128, 255), (10, 35, mana_width, 20))
        mana_text = font.render(f"Maná: {player.mana}/{player.max_mana}", True, (255, 255, 255))
        screen.blit(mana_text, (15, 37))

    # Barra de experiencia
    if player.clase != "Aspirante":
        xp_y = 60 if player.max_mana > 0 else 35
        pygame.draw.rect(screen, (30, 30, 30), (10, xp_y, 200, 15))
        xp_width = (player.xp / player.xp_to_next_level) * 200
        pygame.draw.rect(screen, (0, 255, 255), (10, xp_y, xp_width, 15))
        xp_text = font.render(f"Nvl {player.level} - XP: {player.xp}/{player.xp_to_next_level}", True, (255, 255, 255))
        screen.blit(xp_text, (15, xp_y))
    
    # Hotbar con tooltips
    HOTBAR_SLOT_SIZE = 40
    HOTBAR_PADDING = 5
    hotbar_width = (HOTBAR_SLOT_SIZE + HOTBAR_PADDING) * 9
    hotbar_x = (s.WIDTH - hotbar_width) // 2
    hotbar_y = s.HEIGHT - HOTBAR_SLOT_SIZE - 10
    
    mx, my = pygame.mouse.get_pos()
    
    for i in range(9):
        slot_x = hotbar_x + i * (HOTBAR_SLOT_SIZE + HOTBAR_PADDING)
        slot_rect = pygame.Rect(slot_x, hotbar_y, HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE)
        pygame.draw.rect(screen, (0, 0, 0, 150), slot_rect) 
        
        item = player.hotbar[i]
        if item:
            # Usar sprite si existe, sino usar color
            if item['name'] in s.SPRITES:
                sprite = s.SPRITES[item['name']]
                # Escalar sprite al tamaño del slot
                scaled_sprite = pygame.transform.scale(sprite, (HOTBAR_SLOT_SIZE - 8, HOTBAR_SLOT_SIZE - 8))
                screen.blit(scaled_sprite, (slot_x + 4, hotbar_y + 4))
            else:
                item_color_key = item['name'] if item['id'] is None else item['id']
                item_color = s.COLORS.get(item_color_key, (255,0,255))
                pygame.draw.rect(screen, item_color, slot_rect.inflate(-8, -8))
            
            count_text = font.render(str(item['count']), True, (255, 255, 255))
            screen.blit(count_text, (slot_x + HOTBAR_SLOT_SIZE - count_text.get_width() - 5, hotbar_y + HOTBAR_SLOT_SIZE - count_text.get_height() - 5))
            
            # Tooltip MÁS PEQUEÑO para items en hotbar
            if slot_rect.collidepoint(mx, my):
                tooltip_text = f"{item['name']}"
                tooltip_manager.set_tooltip(tooltip_text)
            
        if i == player.hotbar_selected:
            pygame.draw.rect(screen, (255, 255, 0), slot_rect, 3)

def draw_inventory_screen(screen, player, font, title_font, crafting_ui, tooltip_manager):
    s_surf = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
    s_surf.fill((0, 0, 0, 180)) 
    screen.blit(s_surf, (0, 0))
    
    title = title_font.render("Inventario y Crafteo", True, (255, 255, 255))
    screen.blit(title, ((s.WIDTH - title.get_width()) // 2, 50))

    craft_title = font.render("Recetas Disponibles (Clic para craftear):", True, (255, 255, 255))
    screen.blit(craft_title, (100, 150))
    crafting_ui.draw(screen, player, tooltip_manager)

    # Inventario
    INV_SLOT_SIZE = 40
    INV_PADDING = 5
    inv_cols = 9
    inv_rows = 3
    inv_x_start = (s.WIDTH - (inv_cols * (INV_SLOT_SIZE + INV_PADDING))) // 2
    inv_y_start = s.HEIGHT - 200 
    
    items = list(player.inventory.items())
    slot_index = 0
    
    mx, my = pygame.mouse.get_pos()
    
    for y in range(inv_rows):
        for x in range(inv_cols):
            slot_rect = pygame.Rect(
                inv_x_start + x * (INV_SLOT_SIZE + INV_PADDING),
                inv_y_start + y * (INV_SLOT_SIZE + INV_PADDING),
                INV_SLOT_SIZE, INV_SLOT_SIZE
            )
            pygame.draw.rect(screen, (50, 50, 50), slot_rect)
            
            if slot_index < len(items):
                item_name, count = items[slot_index]
                
                # Usar sprite si existe, sino usar color
                if item_name in s.SPRITES:
                    sprite = s.SPRITES[item_name]
                    scaled_sprite = pygame.transform.scale(sprite, (INV_SLOT_SIZE - 8, INV_SLOT_SIZE - 8))
                    screen.blit(scaled_sprite, (slot_rect.x + 4, slot_rect.y + 4))
                else:
                    item_color = s.COLORS.get(item_name, (255, 0, 255))
                    pygame.draw.rect(screen, item_color, slot_rect.inflate(-4, -4))
                
                count_text = font.render(str(count), True, (255, 255, 255))
                screen.blit(count_text, (slot_rect.x + 2, slot_rect.y + 2))
                
                # Tooltip para items en inventario
                if slot_rect.collidepoint(mx, my):
                    tooltip_text = f"{item_name}\nCantidad: {count}"
                    tooltip_manager.set_tooltip(tooltip_text)
            
            slot_index += 1

    # Hotbar en inventario
    hotbar_y = inv_y_start + inv_rows * (INV_SLOT_SIZE + INV_PADDING) + 10
    for i in range(9):
        slot_x = inv_x_start + i * (INV_SLOT_SIZE + INV_PADDING)
        slot_rect = pygame.Rect(slot_x, hotbar_y, INV_SLOT_SIZE, INV_SLOT_SIZE)
        pygame.draw.rect(screen, (30, 30, 30), slot_rect)
        item = player.hotbar[i]
        if item:
            # Usar sprite si existe, sino usar color
            if item['name'] in s.SPRITES:
                sprite = s.SPRITES[item['name']]
                scaled_sprite = pygame.transform.scale(sprite, (INV_SLOT_SIZE - 8, INV_SLOT_SIZE - 8))
                screen.blit(scaled_sprite, (slot_rect.x + 4, slot_rect.y + 4))
            else:
                item_color_key = item['name'] if item['id'] is None else item['id']
                item_color = s.COLORS.get(item_color_key, (255,0,255))
                pygame.draw.rect(screen, item_color, slot_rect.inflate(-4, -4))
            
            count_text = font.render(str(item['count']), True, (255, 255, 255))
            screen.blit(count_text, (slot_x + 2, hotbar_y + 2))

def draw_class_selection(screen, font, title_font):
    s_surf = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
    s_surf.fill((0, 0, 0, 180)) 
    screen.blit(s_surf, (0, 0))
    title = title_font.render("Elige tu Camino", True, (255, 255, 255))
    screen.blit(title, ((s.WIDTH - title.get_width()) // 2, 100))
    options = ["1. Guerrero - Más vida y daño cuerpo a cuerpo", 
               "2. Mago - Maná y hechizos poderosos", 
               "3. Alquimista - Bonus al crafteo de pociones", 
               "4. Arquero - Precisión y armas a distancia"]
    y_pos = 200
    for text in options:
        text_surf = font.render(text, True, (255, 255, 255))
        screen.blit(text_surf, ((s.WIDTH - text_surf.get_width()) // 2, y_pos))
        y_pos += 40