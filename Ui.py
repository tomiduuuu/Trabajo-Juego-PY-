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
            
    def draw(self, screen, player):
        y_pos = 180
        for recipe_name, rect in self.recipe_rects.items():
            can_craft = True
            recipe = s.RECIPES[recipe_name]
            for material, amount in recipe["materials"].items():
                if player.inventory.get(material, 0) < amount:
                    can_craft = False
                    break
            
            color = (0, 150, 0) if can_craft else (150, 0, 0)
            pygame.draw.rect(screen, color, rect)
            
            text = f"{recipe_name} ({recipe['count']}x)"
            text_surf = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 7))
            
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
        
        if player.clase == "Alquimista": player.add_xp(100)
        else: player.add_xp(20)

# --- Funciones de Dibujado de UI ---

def draw_hud(screen, player, font):
    pygame.draw.rect(screen, (50, 0, 0), (10, 10, 200, 20))
    health_width = (player.health / player.max_health) * 200
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_width, 20))
    
    if player.max_mana > 0:
        pygame.draw.rect(screen, (0, 0, 50), (10, 35, 200, 20))
        mana_width = (player.mana / player.max_mana) * 200
        pygame.draw.rect(screen, (0, 128, 255), (10, 35, mana_width, 20))

    if player.clase != "Aspirante":
        xp_y = 60 if player.max_mana > 0 else 35
        pygame.draw.rect(screen, (30, 30, 30), (10, xp_y, 200, 15))
        xp_width = (player.xp / player.xp_to_next_level) * 200
        pygame.draw.rect(screen, (0, 255, 255), (10, xp_y, xp_width, 15))
    
    HOTBAR_SLOT_SIZE = 40
    HOTBAR_PADDING = 5
    hotbar_width = (HOTBAR_SLOT_SIZE + HOTBAR_PADDING) * 9
    hotbar_x = (s.WIDTH - hotbar_width) // 2
    hotbar_y = s.HEIGHT - HOTBAR_SLOT_SIZE - 10
    
    for i in range(9):
        slot_x = hotbar_x + i * (HOTBAR_SLOT_SIZE + HOTBAR_PADDING)
        slot_rect = pygame.Rect(slot_x, hotbar_y, HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE)
        pygame.draw.rect(screen, (0, 0, 0, 150), slot_rect) 
        
        item = player.hotbar[i]
        if item:
            item_color_key = item['name'] if item['id'] is None else item['id']
            item_color = s.COLORS.get(item_color_key, (255,0,255))
            pygame.draw.rect(screen, item_color, slot_rect.inflate(-8, -8))
            count_text = font.render(str(item['count']), True, (255, 255, 255))
            screen.blit(count_text, (slot_x + HOTBAR_SLOT_SIZE - count_text.get_width() - 5, hotbar_y + HOTBAR_SLOT_SIZE - count_text.get_height() - 5))
            
        if i == player.hotbar_selected:
            pygame.draw.rect(screen, (255, 255, 0), slot_rect, 3) 

def draw_inventory_screen(screen, player, font, title_font, crafting_ui):
    s_surf = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
    s_surf.fill((0, 0, 0, 180)) 
    screen.blit(s_surf, (0, 0))
    
    title = title_font.render("Inventario y Crafteo", True, (255, 255, 255))
    screen.blit(title, ((s.WIDTH - title.get_width()) // 2, 50))

    craft_title = font.render("Recetas Disponibles (Clic para craftear):", True, (255, 255, 255))
    screen.blit(craft_title, (100, 150))
    crafting_ui.draw(screen, player) 

    INV_SLOT_SIZE = 40
    INV_PADDING = 5
    inv_cols = 9
    inv_rows = 3
    inv_x_start = (s.WIDTH - (inv_cols * (INV_SLOT_SIZE + INV_PADDING))) // 2
    inv_y_start = s.HEIGHT - 200 
    
    items = list(player.inventory.items())
    slot_index = 0
    
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
                item_color = s.COLORS.get(item_name, (255, 0, 255))
                pygame.draw.rect(screen, item_color, slot_rect.inflate(-4, -4))
                count_text = font.render(str(count), True, (255, 255, 255))
                screen.blit(count_text, (slot_rect.x + 2, slot_rect.y + 2))
            
            slot_index += 1

    hotbar_y = inv_y_start + inv_rows * (INV_SLOT_SIZE + INV_PADDING) + 10
    for i in range(9):
        slot_x = inv_x_start + i * (INV_SLOT_SIZE + INV_PADDING)
        slot_rect = pygame.Rect(slot_x, hotbar_y, INV_SLOT_SIZE, INV_SLOT_SIZE)
        pygame.draw.rect(screen, (30, 30, 30), slot_rect)
        item = player.hotbar[i]
        if item:
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
    options = ["1. Guerrero", "2. Mago", "3. Alquimista", "4. Arquero"]
    y_pos = 200
    for text in options:
        text_surf = font.render(text, True, (255, 255, 255))
        screen.blit(text_surf, ((s.WIDTH - text_surf.get_width()) // 2, y_pos))
        y_pos += 40
